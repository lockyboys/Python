# [image_analyzer.py] - AI 이미지 분석 모듈 (v23 - Full Lock)
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
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
    TF_READY = True
    AI_READY = True
except: pass

model = None

def load_tf_model():
    global model
    if not TF_READY: return
    try:
        model = MobileNetV2(weights='imagenet')
    except Exception as e:
        utils.log_error(f"TF 모델 로딩 실패: {e}")

AI_CATEGORIES = {
    "01_중요문서_및_행정": ["envelope", "web_site", "menu", "book_jacket", "crossword_puzzle"],
    "02_동물_및_생물": ["dog", "cat", "bird", "fish", "butterfly", "insect", "animal", "pet"],
    "03_풍경_및_자연": ["valley", "mountain", "alp", "volcano", "promontory", "lakeside", "seashore", "ocean", "tree"],
    "04_음식_및_요리": ["food", "plate", "dish", "burrito", "pizza", "guacamole", "ice_cream", "bakery"],
    "05_가구_및_사물": ["desk", "table", "chair", "laptop", "monitor", "mouse", "keyboard", "cellular_telephone"],
    "06_기타_이미지": []
}

def analyze_image_final(image_path):
    try:
        # [핵심] 경로 기반 제외 체크
        if utils.is_excluded(image_path): return None
        
        name = image_path.name.lower()
        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw.lower() in name for kw in kws): return folder

        if TF_READY:
            if model is None: load_tf_model()
            img = Image.open(image_path).convert('RGB').resize((224, 224))
            x = preprocess_input(np.expand_dims(tf.keras.preprocessing.image.img_to_array(img), axis=0))
            preds = model.predict(x, verbose=0)
            results = decode_predictions(preds, top=3)[0]
            for _, label, score in results:
                label = label.lower()
                for category, keywords in AI_CATEGORIES.items():
                    if any(kw in label for kw in keywords): return category
    except Exception as e:
        utils.log_error(f"이미지 분석 오류 ({image_path.name}): {e}")
    return "09_일반_사진"

def run_image_ai_organizing(target_path):
    target = Path(target_path)
    count = 0
    ai_root = target / "AI_TF_분석결과"
    print("🧠 AI 이미지 정밀 분석 중...")
    try:
        pattern = '**/*' if (config.RECURSIVE_SCAN or config.UNPACK_ALL) else '*'
        img_files = [f for f in target.glob(pattern) if f.is_file() and f.suffix.lower() in config.IMAGE_EXTENSIONS]
        for item in img_files:
            # [핵심] 경로 기반 제외 체크
            if utils.is_excluded(item): continue
            
            if not config.UNPACK_ALL:
                if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹')) for p in item.parents if p != target):
                    continue
            category = analyze_image_final(item)
            if not category: continue
            
            if category in AI_CATEGORIES or category == "09_일반_사진":
                utils.move_file(item, ai_root / category)
            else:
                utils.move_file(item, target / category)
            count += 1
    except Exception as e:
        utils.log_error(f"이미지 AI 정리 프로세스 오류: {e}")
    return count
