# [image_analyzer.py] - OCR(글자 인식) 기반 지능형 이미지 분석 모듈
import os
import time
import config
import utils
from pathlib import Path
from PIL import Image, ImageStat

# OCR 라이브러리 연결
try:
    import pytesseract
except ImportError:
    pytesseract = None

def get_image_visual_features(image_path):
    """이미지를 직접 열어 시각적 특징(밝기, 색상, 대비)을 추출합니다."""
    try:
        with Image.open(image_path) as img:
            # 1. 분석을 위해 이미지를 작게 리사이즈 (속도 향상)
            img_small = img.resize((100, 100)).convert('RGB')
            stat = ImageStat.Stat(img_small)
            
            # 평균 밝기 (0-255)
            avg_brightness = sum(stat.mean) / 3
            
            # 색상 표준편차 (대비/복잡도 지표)
            std_dev = sum(stat.stddev) / 3
            
            # 흰색 배경 비중 확인 (문서 판별용)
            # 밝기가 매우 높고 색상 차이가 적은 픽셀 수 계산
            extrema = img_small.getextrema()
            is_high_contrast = (extrema[0][1] - extrema[0][0]) > 200 # 대비가 큰지
            
            result = {
                'brightness': avg_brightness,
                'complexity': std_dev,
                'is_bright': avg_brightness > 200,
                'is_document_like': avg_brightness > 180 and std_dev < 50
            }
            print(f"▶ ->📊 {image_path.name}  이미지 열기 성공")
            return result
    except Exception as e:
        print(f"▷->⚠️ {image_path.name} 분석 중 오류: {e}")
        return None


def extract_text(image_path):
    """이미지에서 글자를 읽어옵니다 (OCR)."""
    if not pytesseract: return ""
    try:
        # Additional language data 체크 또는 kor.traineddata 필요. 보통 위치: C:\Program Files\Tesseract-OCR\tesseract.exe
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )
        # 한국어와 영어를 함께 인식하도록 설정 
        print(f"▶->📄 {image_path.name} - OCR 인식 결과: 성공")  # 앞부분만 출력
        return pytesseract.image_to_string(Image.open(image_path), lang='kor+eng').strip()
    except:
        print(f"▷->📄 {image_path.name} - OCR 인식 결과: 오류")  # 앞부분만 출력
        return "" 

def analyze_image_ai(image_path):
    """시각 분석 + OCR + 키워드를 결합한 최종 AI 판단 로직"""
    name = image_path.name
    
    # -1. 이미지 열기 및 시각 분석
    time.sleep(0.1) # 잠시 쉬도록한다.
    
    features = get_image_visual_features(image_path)
    
    time.sleep(0.1) # 잠시 쉬도록한다.

    # 0. OCR 글자 읽기
    text_content = extract_text(image_path)

    time.sleep(0.1) # 잠시 쉬도록한다.

    # 1. 문서 AI 분석 (이미지 내 텍스트 및 파일명 패턴)
    doc_keywords = config.KEYWORD_RULES_IMP_DOC #["신분증", "계약서", "등록증", "확인서", "영수증", "통지서", "필증", "검진"]
    if any(kw in text_content or kw in name for kw in doc_keywords):
        return "01_AI_분석_문서"
    
    time.sleep(0.1) # 잠시 쉬도록한다.

    # 2. AI 생성 이미지 식별
    doc_keywords = config.KEYWORD_RULES_AI #["ChatGPT", "Gemini", "DALL-E", "Generated", "AI"]
    if any(kw in text_content or kw in name for kw in doc_keywords):
        return "02.AI_생성_문서"

    time.sleep(0.1) # 잠시 쉬도록한다.

    # 3. 메신저 및 스크린샷 식별
        # 1. 문서 AI 분석 (이미지 내 텍스트 및 파일명 패턴)
    doc_keywords = config.KEYWORD_RULES_IMP_DOC #["신분증", "계약서", "등록증", "확인서", "영수증", "통지서", "필증", "검진"]
    if any(kw in text_content or kw in name for kw in doc_keywords):
        return "03.AI_분석_문서"

    time.sleep(0.1) # 잠시 쉬도록한다.

    # 4. AI 생성 이미지 식별
    doc_keywords = config.KEYWORD_RULES_AI #["ChatGPT", "Gemini", "DALL-E", "Generated", "AI"]
    if any(kw in text_content or kw in name for kw in doc_keywords):
        return "04.AI_생성_인공지능_문서"
    
    time.sleep(0.1) # 잠시 쉬도록한다.

    # 5. 메신저 및 스크린샷 식별
    messenger_keywords = config.KEYWORD_RULES_MESSEGER # if "KakaoTalk" in filename or "Screenshot" in filename:["KakaoTalk", "LINE", "카톡", "라인"]
    if any(kw in text_content or kw in name for kw in messenger_keywords):
        return "05.AI_분석_메신저_스크린샷_문서"
    
    time.sleep(0.1) # 잠시 쉬도록한다.

    print(f"★->🔍 {name} - AI 분석 결과: 일반 사진으로 분류됨.")
    # [단계 2] 시각적 특징 기반 2차 분류 (AI 로직)
    if features:
        print(f"♥->📊 {name} - 밝기: {features['brightness']:.1f}, 복잡도: {features['complexity']:.1f}")
        # 밝기가 매우 높고 복잡도가 낮으면 문서(스캔본/스크린샷)로 판단
        if features['is_document_like'] or "Screenshot" in name:
            return "06_문서_및_스크린샷"
        
        time.sleep(0.1) # 잠시 쉬도록한다.

        # 복잡도가 매우 높으면 화려한 디자인이나 사진으로 판단
        if features['complexity'] > 70:
            return "07_화려한_디자인_및_사진"

        # 밝기가 낮으면 어두운 사진이나 밤 배경
        if features['brightness'] < 80:
            return "08_어두운_테마_사진"
        
        time.sleep(0.1) # 잠시 쉬도록한다.

    # [단계 3] 기본 분류
    return "09_일반_기타_사진"

def run_image_ai_organizing(target_path):
    """메인 컨트롤러에서 호출하는 실행 함수"""
    target = Path(target_path)
    count = 0
    
    print("🧠 AI가 이미지 속의 글자를 읽고 있습니다 (OCR 분석 중)...")
    
    for item in target.iterdir():
        if item.is_dir() or item.suffix.lower() not in config.IMAGE_EXTENSIONS:
            continue
        
        time.sleep(0.1) # 잠시 쉬도록한다.

        # OCR 및 AI 시각 분석 실행
        category = analyze_image_ai(item)
        
        time.sleep(0.1) # 잠시 쉬도록한다.

        # 분석 결과 폴더로 이동
        dest_folder = target / "AI_시각분석_결과" / category
        utils.move_file(item, dest_folder)
        count += 1
        
    return count