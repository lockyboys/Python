# [image_analyzer.py] - TensorFlow AI 기반 객체 인식 및 OCR 통합 모듈 (v10)
import os
import config
import utils
from pathlib import Path

# 1. 라이브러리 연결 (오류 방지용 예외 처리 강화)
AI_READY = False
TF_READY = False
OCR_READY = False

try:
    import numpy as np
    from PIL import Image
    AI_READY = True
except ImportError:
    print("⚠️ 알림: 'numpy' 또는 'Pillow' 라이브러리가 설치되지 않았습니다. 기본 분석 모드로 작동합니다.")

try:
    import tensorflow as tf
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
    TF_READY = True
except ImportError:
    pass

try:
    import pytesseract
    OCR_READY = True
except ImportError:
    pass

# 2. AI 모델 로드
model = None

def load_tf_model():
    global model
    if not TF_READY: return
    try:
        model = MobileNetV2(weights='imagenet')
    except Exception as e:
        print(f"⚠️ TensorFlow 모델 로딩 실패: {e}")

def get_tf_prediction(image_path):
    """TensorFlow AI가 사진을 보고 무엇인지 판단합니다."""
    global model
    if not (TF_READY and AI_READY): return "09_일반_사진"
    if model is None: load_tf_model()
    if model is None: return "09_일반_사진"
    
    try:
        import numpy as np
        img = Image.open(image_path).convert('RGB').resize((224, 224))
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = model.predict(x, verbose=0)
        decoded = decode_predictions(preds, top=1)[0][0]
        label = decoded[1].lower()
        
        if any(word in label for word in ['dog', 'cat', 'bird', 'animal', 'horse', 'elephant', 'panda']):
            return "07_동물_및_생물"
        if any(word in label for word in ['valley', 'mountain', 'ocean', 'coast', 'forest', 'lake', 'cliff', 'tree']):
            return "08_풍경_및_자연"
        if any(word in label for word in ['food', 'plate', 'dish', 'pizza', 'burger', 'cake']):
            return "10_음식_및_요리"
        if any(word in label for word in ['chair', 'table', 'desk', 'laptop', 'monitor', 'keyboard']):
            return "11_가구_및_사물"
        
        return "09_일반_사진"
    except:
        return "09_일반_사진"

def analyze_image_final(image_path):
    """[OCR 글자 인식] + [TensorFlow 객체 인식] 통합 판단"""
    name = image_path.name.lower()
    
    # [단계 1] 파일명 키워드 우선 확인 (가장 빠름)
    for folder, kws in config.KEYWORD_RULES.items():
        if any(kw.lower() in name for kw in kws):
            return folder

    # [단계 2] OCR 글자 읽기 (문서 판별)
    if OCR_READY and AI_READY:
        try:
            from PIL import Image
            text_content = pytesseract.image_to_string(Image.open(image_path), lang='kor+eng').strip().lower()
            # 중요 문서 키워드 확인
            for folder, kws in config.KEYWORD_RULES.items():
                if any(kw.lower() in text_content for kw in kws):
                    return folder
        except: pass
    
    # [단계 3] TensorFlow AI 이미지 분석
    if TF_READY:
        return get_tf_prediction(image_path)
        
    return "09_일반_사진"

def run_image_ai_organizing(target_path):
    """메인 컨트롤러에서 호출하는 실행 함수"""
    target = Path(target_path)
    count = 0
    
    print("🧠 AI 분석 엔진 가동 중 (파일명/글자/이미지 내용 통합 분석)...")
    
    # 싹쓸이 모드: 하위 폴더까지 모든 이미지 탐색
    image_files = [f for f in target.rglob('*') if f.is_file() and f.suffix.lower() in config.IMAGE_EXTENSIONS]
    
    for item in image_files:
        # 이미 분류된 폴더 안에 있는 경우 제외
        if any(p.name.startswith(('0', '1', 'AI_TF')) for p in item.parents if p != target):
            continue
            
        category = analyze_image_final(item)
        
        # 결과 폴더로 이동 (사용자 소스 구조 유지)
        dest_folder = target / "AI_TF_분석결과" / category
        utils.move_file(item, dest_folder)
        count += 1
        
    return count
