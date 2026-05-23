# [image_analyzer.py] - AI 이미지 정밀 분석 모듈 (v24 - Restore Precision)
import os
import utils
import config
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

AI_READY = False
TF_READY = False
GPU_ACTIVE = False

try:
    import numpy as np
    from PIL import Image
    import tensorflow as tf
    tf.config.threading.set_inter_op_parallelism_threads(4)
    tf.config.threading.set_intra_op_parallelism_threads(4)
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus: tf.config.experimental.set_memory_growth(gpu, True)
        GPU_ACTIVE = True
    from tensorflow.keras.applications.efficientnet import EfficientNetB0, preprocess_input, decode_predictions
    TF_READY = True
    AI_READY = True
except: pass

model = None

def load_tf_model():
    global model
    if not TF_READY: return
    try:
        model = EfficientNetB0(weights='imagenet')
    except Exception as e:
        utils.log_error(f"TF 모델 로딩 실패: {e}")

# [복구] 사용자님이 가장 만족하셨던 정밀 카테고리 체계
AI_CATEGORIES = {
    "01_중요문서_및_행정": ["id_card", "passport", "envelope"],
    "02_동물_및_생물": ["dog", "cat", "bird", "fish", "butterfly", "insect", "animal", "pet", "lion", "tiger", "bear"],
    "03_풍경_및_자연": ["valley", "mountain", "alp", "volcano", "promontory", "lakeside", "seashore", "ocean", "tree", "forest", "sky", "cloud"],
    "04_음식_및_요리": ["food", "plate", "dish", "burrito", "pizza", "guacamole", "ice_cream", "bakery", "cake", "fruit"],
    "05_가구_및_사물": ["desk", "table", "chair", "laptop", "monitor", "mouse", "keyboard", "cellular_telephone", "car", "bicycle"],
    "06_기타_이미지": []
}

# def analyze_image_final(image_path):

#     try:

#         if utils.is_excluded(image_path):
#             return None

#         # ⭐ 작은 파일은 AI 안 돌림
#         if image_path.stat().st_size < 30000:
#             return "09_일반_사진"

#         # ⭐ 파일명 우선 검사
#         name = image_path.name.lower()

#         for folder, kws in config.KEYWORD_RULES.items():
#             if any(kw.lower() in name for kw in kws):
#                 return folder

#         # ⭐ AI 분석
#         if TF_READY:

#             global model

#             if model is None:
#                 load_tf_model()

#             img = Image.open(image_path).convert('RGB')

#             # ⭐ 강제 크기 고정
#             img = img.resize((224, 224))

#             x = preprocess_input(
#                 np.expand_dims(
#                     tf.keras.preprocessing.image.img_to_array(img),
#                     axis=0
#                 )
#             )

#             preds = model.predict(x, verbose=0)

#             results = decode_predictions(preds, top=3)[0]

#             for _, label, score in results:

#                 # ⭐ 정확도 낮으면 무시
#                 if score < 0.45:
#                     continue

#                 label = label.lower()

#                 for category, keywords in AI_CATEGORIES.items():
#                     if any(kw in label for kw in keywords):
#                         return category

#     except Exception as e:
#         utils.log_error(f"이미지 분석 오류 ({image_path.name}): {e}")

#     return "09_일반_사진"

def analyze_image_final(image_path):

    try:

        if utils.is_excluded(image_path):
            return None

        # 작은 파일은 AI 분석 안 함
        if image_path.stat().st_size < 30000:
            return "09_일반_사진"

        # 파일명 우선 검사
        name = image_path.name.lower()

        for folder, kws in config.KEYWORD_RULES.items():

            if any(
                kw.lower() in name
                for kw in kws
            ):
                return folder

        if TF_READY:

            global model

            if model is None:
                load_tf_model()

            img = Image.open(image_path).convert('RGB')

            # 크기 고정
            img = img.resize((224, 224))

            x = preprocess_input(
                np.expand_dims(
                    tf.keras.preprocessing.image.img_to_array(img),
                    axis=0
                )
            )

            preds = model.predict(x, verbose=0)

            results = decode_predictions(
                preds,
                top=3
            )[0]

            for _, label, score in results:

                # 정확도 낮으면 무시
                if score < 0.45:
                    continue

                label = label.lower()

                for category, keywords in AI_CATEGORIES.items():

                    if any(
                        kw in label
                        for kw in keywords
                    ):
                        return category

    except Exception as e:
        utils.log_error(
            f"이미지 분석 오류 ({image_path.name}): {e}"
        )

    return "09_일반_사진"

# def process_single_image(args):

#     item, target = args

#     try:
#         category = analyze_image_final(item)

#         if not category:
#             return 0

#         ai_root = target / "AI_TF_분석결과"

#         # AI 카테고리
#         if category in AI_CATEGORIES or category == "09_일반_사진":
#             utils.move_file(item, ai_root / category)

#         else:
#             utils.move_file(item, target / category)

#         return 1

#     except Exception as e:
#         utils.log_error(f"이미지 처리 오류 ({item.name}): {e}")
#         return 0

def process_single_image(args):

    item, target = args

    try:
        category = analyze_image_final(item)

        if not category:
            return 0

        ai_root = target / "AI_TF_분석결과"

        utils.move_file(
            item,
            ai_root / category
        )

        return 1

    except Exception as e:

        utils.log_error(
            f"이미지 처리 오류 ({item.name}): {e}"
        )

        return 0


def run_image_ai_organizing(
    target_path,
    img_files
):

    target = Path(target_path)

    count = 0

    print("🧠 멀티스레드 이미지 분석 중...")

    # ⭐ 동시에 4개 처리
    with ThreadPoolExecutor(
        max_workers=4
    ) as executor:

        results = executor.map(
            process_single_image,
            [(item, target) for item in img_files]
        )

        count = sum(results)

    return count

# def run_image_ai_organizing(target_path, img_files):

#     target = Path(target_path)

#     print("🧠 멀티스레드 이미지 분석 중...")

#     count = 0

#     # ⭐ 컴퓨터 4명이 동시에 일함
#     with ThreadPoolExecutor(max_workers=4) as executor:

#         results = executor.map(
#             process_single_image,
#             [(item, target) for item in img_files]
#         )

#         count = sum(results)

#     return count
