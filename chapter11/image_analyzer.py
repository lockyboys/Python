# [image_analyzer.py] - AI 이미지 정밀 분석 모듈 (v20 - Restore AI Categories)
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

# 정밀 분류 카테고리 매핑
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
        if image_path.name in config.EXCLUDE_LIST: return None
        
        # 1단계: 키워드 기반 분류 (신분증 등 중요 문서 보호)
        name = image_path.name.lower()
        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw.lower() in name for kw in kws): return folder

        # 2단계: AI 정밀 분석
        if TF_READY:
            if model is None: load_tf_model()
            img = Image.open(image_path).convert('RGB').resize((224, 224))
            x = preprocess_input(np.expand_dims(tf.keras.preprocessing.image.img_to_array(img), axis=0))
            preds = model.predict(x, verbose=0)
            results = decode_predictions(preds, top=3)[0]
            
            for _, label, score in results:
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
    print("🧠 AI 이미지 정밀 분석 및 분류 중...")
    
    try:
        pattern = '**/*' if (config.RECURSIVE_SCAN or config.UNPACK_ALL) else '*'
        img_files = [f for f in target.glob(pattern) if f.is_file() and f.suffix.lower() in config.IMAGE_EXTENSIONS]
        
        for item in img_files:
            if item.name in config.EXCLUDE_LIST: continue
            
            # 이미 분류된 폴더 제외 (해체 모드가 아닐 때)
            if not config.UNPACK_ALL:
                if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹')) for p in item.parents if p != target):
                    continue
            
            category = analyze_image_final(item)
            
            # AI 분류 결과인 경우 AI_TF_분석결과 폴더 아래로, 아니면 루트 하위로
            if category in AI_CATEGORIES or category == "09_일반_사진":
                utils.move_file(item, ai_root / category)
            else:
                utils.move_file(item, target / category)
            
            count += 1
    except Exception as e:
        utils.log_error(f"이미지 AI 정리 프로세스 오류: {e}")
    return count
