# [image_analyzer.py] - TensorFlow AI 기반 객체 인식 및 OCR 통합 모듈
import os
import config
import utils
import numpy as np
from pathlib import Path
from PIL import Image

# 1. TensorFlow 및 라이브러리 연결...
try:
    import tensorflow as tf
    from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
    import pytesseract
except ImportError:
    print("알림: TensorFlow 또는 관련 라이브러리가 설치되지 않았습니다.")

# 2. AI 모델 로드
model = None

def load_tf_model():
    global model
    try:
        # 사전 학습된 MobileNetV2 모델 로드 (이미지넷 데이터셋 기반)
        model = MobileNetV2(weights='imagenet')
    except Exception as e:
        print(f"⚠️ TensorFlow 모델 로딩 실패: {e}")

def get_tf_prediction(image_path):
    """TensorFlow AI가 사진을 보고 무엇인지 판단합니다."""
    global model
    if model is None: load_tf_model()
    
    try:
        # 이미지 불러오기 및 전처리 (224x224 사이즈)
        img = Image.open(image_path).convert('RGB')
        img = img.resize((224, 224))
        x = tf.keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # 예측 실행
        preds = model.predict(x, verbose=0)
        # 상위 1개 결과 추출
        decoded = decode_predictions(preds, top=1)[0][0]
        label = decoded[1] # 클래스 이름
        
        # 클래스 이름을 한국어 카테고리로 매핑 (단순화)
        if any(word in label for word in ['dog', 'cat', 'bird', 'animal', 'horse', 'elephant']):
            return "02_동물_및_생물"
        if any(word in label for word in ['valley', 'mountain', 'ocean', 'coast', 'forest', 'lake']):
            return "03_풍경_및_자연"
        if any(word in label for word in ['food', 'plate', 'dish', 'pizza', 'burger']):
            return "04_음식_및_요리"
        if any(word in label for word in ['chair', 'table', 'desk', 'laptop', 'monitor']):
            return "05_가구_및_사물"
        
        return "06_기타_이미지"
    except Exception as e:
        return "06_기타_이미지"

def analyze_image_final(image_path):
    """[OCR 글자 인식] + [TensorFlow 객체 인식] 통합 판단"""
    name = image_path.name
    
    # [단계 1] OCR 글자 읽기 (문서 판별 우선)
    text_content = ""
    try:
        text_content = pytesseract.image_to_string(Image.open(image_path), lang='kor+eng').strip()
    except: pass
    
    # [단계 2] 중요 문서 키워드 확인
    doc_keywords = ["계약", "신분증", "주민등록", "사업자", "영수증", "확인서", "등본", "신고필증"]
    if any(kw in text_content or kw in name for kw in doc_keywords):
        return "01_중요문서_및_행정"

    # [단계 3] TensorFlow AI 이미지 분석
    return get_tf_prediction(image_path)

def run_image_ai_organizing(target_path):
    """메인 컨트롤러에서 호출하는 실행 함수"""
    target = Path(target_path)
    count = 0
    
    print("🧠 TensorFlow AI가 사진 속 물체를 분석 중입니다...")
    
    for item in target.iterdir():
        if item.is_dir() or item.suffix.lower() not in config.IMAGE_EXTENSIONS:
            continue
        
        # 최종 통합 AI 분석 실행
        category = analyze_image_final(item)
        
        # 결과 폴더로 이동
        dest_folder = target / "AI_TF_분석결과" / category
        utils.move_file(item, dest_folder)
        count += 1
        
    return count
