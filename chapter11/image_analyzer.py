# [image_analyzer.py] - AI 이미지 분석 모듈 (v16)
import os
import config
import utils
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
        utils.log_message(f"TF 모델 로딩 실패: {e}", "ERROR")

def analyze_image_final(image_path):
    try:
        if image_path.name in config.EXCLUDE_LIST: return None
        
        name = image_path.name.lower()
        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw.lower() in name for kw in kws): return folder

        if TF_READY:
            if model is None: load_tf_model()
            img = Image.open(image_path).convert('RGB').resize((224, 224))
            x = preprocess_input(np.expand_dims(tf.keras.preprocessing.image.img_to_array(img), axis=0))
            preds = model.predict(x, verbose=0)
            label = decode_predictions(preds, top=1)[0][0][1].lower()
            
            if any(w in label for w in ['dog', 'cat', 'animal']): return "07_동물_및_생물"
            if any(w in label for w in ['mountain', 'tree', 'nature']): return "08_풍경_및_자연"
            if any(w in label for w in ['food', 'dish']): return "10_음식_및_요리"
    except Exception as e:
        utils.log_message(f"이미지 분석 오류 ({image_path.name}): {e}", "ERROR")
    return "09_일반_사진"

def run_image_ai_organizing(target_path):
    target = Path(target_path)
    count = 0
    try:
        pattern = '**/*' if config.RECURSIVE_SCAN else '*'
        files = [f for f in target.glob(pattern) if f.is_file() and f.suffix.lower() in config.IMAGE_EXTENSIONS]
        for item in files:
            if item.name in config.EXCLUDE_LIST: continue
            if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹')) for p in item.parents if p != target):
                continue
            category = analyze_image_final(item)
            utils.move_file(item, target / "AI_TF_분석결과" / category)
            count += 1
    except Exception as e:
        utils.log_message(f"이미지 프로세스 오류: {e}", "ERROR")
    return count
