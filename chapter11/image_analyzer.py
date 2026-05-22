# [image_analyzer.py] - AI 이미지 분석 모듈 (v15 - Robust Error Handling)
import os
import config
import utils
from pathlib import Path

AI_READY = False
TF_READY = False
OCR_READY = False
GPU_ACTIVE = False

try:
    import numpy as np
    from PIL import Image
    AI_READY = True
except Exception as e:
    utils.log_error(f"이미지 분석 라이브러리 로드 실패: {e}")

try:
    import tensorflow as tf
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        GPU_ACTIVE = True
    
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
    TF_READY = True
except Exception as e:
    utils.log_error(f"TensorFlow 로드 실패: {e}")

try:
    import pytesseract
    OCR_READY = True
except Exception as e:
    utils.log_error(f"Tesseract OCR 로드 실패: {e}")

model = None

def load_tf_model():
    global model
    if not TF_READY: return
    try:
        if GPU_ACTIVE:
            from tensorflow.keras import mixed_precision
            try: mixed_precision.set_global_policy('mixed_float16')
            except: pass
        model = MobileNetV2(weights='imagenet')
    except Exception as e:
        utils.log_error(f"TensorFlow 모델 로딩 실패: {e}")

def get_tf_prediction(image_path):
    global model
    if not (TF_READY and AI_READY): return "09_일반_사진"
    if model is None: load_tf_model()
    if model is None: return "09_일반_사진"
    
    try:
        img = Image.open(image_path).convert('RGB').resize((224, 224))
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = model.predict(x, verbose=0)
        decoded = decode_predictions(preds, top=1)[0][0]
        label = decoded[1].lower()
        
        if any(word in label for word in ['dog', 'cat', 'bird', 'animal', 'horse', 'elephant', 'panda']):
            return "07_동물_및_생물"
        if any(word in label for word in ['valley', 'mountain', 'ocean', 'coast', 'forest', 'lake', 'tree']):
            return "08_풍경_및_자연"
        if any(word in label for word in ['food', 'plate', 'dish', 'pizza', 'cake']):
            return "10_음식_및_요리"
        if any(word in label for word in ['chair', 'table', 'laptop', 'monitor', 'phone']):
            return "11_가구_및_사물"
        return "09_일반_사진"
    except Exception as e:
        utils.log_error(f"이미지 AI 분석 오류 ({image_path.name}): {e}")
        return "09_일반_사진"

def analyze_image_final(image_path):
    try:
        name = image_path.name.lower()
        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw.lower() in name for kw in kws):
                return folder

        if OCR_READY and AI_READY:
            try:
                text = pytesseract.image_to_string(Image.open(image_path), lang='kor+eng').strip().lower()
                for folder, kws in config.KEYWORD_RULES.items():
                    if any(kw.lower() in text for kw in kws):
                        return folder
            except Exception as e:
                utils.log_error(f"OCR 분석 오류 ({image_path.name}): {e}")
        
        if TF_READY:
            return get_tf_prediction(image_path)
    except Exception as e:
        utils.log_error(f"통합 이미지 분석 오류 ({image_path.name}): {e}")
        
    return "09_일반_사진"

def run_image_ai_organizing(target_path):
    target = Path(target_path)
    count = 0
    print("🚀 GPU 가속 AI 이미지 분석 엔진 가동 중..." if GPU_ACTIVE else "🧠 AI 이미지 분석 엔진 가동 중...")
    
    try:
        # RECURSIVE_SCAN 설정 적용
        search_pattern = '**/*' if config.RECURSIVE_SCAN else '*'
        image_files = [f for f in target.glob(search_pattern) if f.is_file() and f.suffix.lower() in config.IMAGE_EXTENSIONS]
        
        for item in image_files:
            if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹')) for p in item.parents if p != target):
                continue
            category = analyze_image_final(item)
            utils.move_file(item, target / "AI_TF_분석결과" / category)
            count += 1
    except Exception as e:
        utils.log_error(f"이미지 정리 프로세스 오류: {e}")
        
    return count
