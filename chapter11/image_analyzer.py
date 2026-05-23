# [image_analyzer.py] - AI 이미지 정밀 분석 모듈 (v24 - Restore Precision)
import os
import utils
import config
from pathlib import Path

AI_READY = False
TF_READY = False
GPU_ACTIVE = False

try:
    import numpy as np
    from PIL import Image
    import tensorflow as tf
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

def analyze_image_final(image_path):

    try:
        if utils.is_excluded(image_path):
            return None

        # 1. 파일명 우선
        name = image_path.name.lower()

        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw.lower() in name for kw in kws):
                return folder

        # 2. AI 분석
        if TF_READY:

            if model is None:
                load_tf_model()

            img = Image.open(image_path).convert('RGB').resize((224, 224))

            x = preprocess_input(
                np.expand_dims(
                    tf.keras.preprocessing.image.img_to_array(img),
                    axis=0
                )
            )

            preds = model.predict(x, verbose=0)
            results = decode_predictions(preds, top=3)[0]

            for _, label, score in results:

                # 정확도 낮으면 무시
                if score < 0.45:
                    continue

                label = label.lower()

                for category, keywords in AI_CATEGORIES.items():
                    if any(kw in label for kw in keywords):
                        return category

    except Exception as e:
        utils.log_error(f"이미지 분석 오류 ({image_path.name}): {e}")

    return "09_일반_사진"

def run_image_ai_organizing(target_path):
    target = Path(target_path)
    count = 0
    ai_root = target / "AI_TF_분석결과"
    print("🧠 AI 이미지 정밀 분석 중 (동물, 풍경, 음식 등)...")
    
    try:
        pattern = '**/*' if (config.RECURSIVE_SCAN or config.UNPACK_ALL) else '*'
        img_files = [f for f in target.glob(pattern) if f.is_file() and f.suffix.lower() in config.IMAGE_EXTENSIONS]
        
        for item in img_files:
            if utils.is_excluded(item): continue
            
            # 이미 분류된 폴더 제외 (해체 모드가 아닐 때)
            if not config.UNPACK_ALL:
                if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹')) for p in item.parents if p != target):
                    continue
            
            category = analyze_image_final(item)
            if not category: continue
            
            # AI 분류 결과는 무조건 AI_TF_분석결과 폴더 하위로
            if category in AI_CATEGORIES or category == "09_일반_사진":
                utils.move_file(item, ai_root / category)
            else:
                # 키워드 기반 결과는 루트 하위로
                utils.move_file(item, target / category)
            
            count += 1
    except Exception as e:
        utils.log_error(f"이미지 AI 정리 프로세스 오류: {e}")
    return count
