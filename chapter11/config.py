# [config.py] - 전체 시스템 설정 파일 (v15 - Control & Logging)

# 1. 키워드 기반 분류 규칙
KEYWORD_RULES = {
    "01_중요문서": ["신분증", "계약서", "등록증", "확인서", "통지서", "등본", "신고필증", "검진", "영수증", "명세서", "증명원", "증명서", "인감", "주민등록", "운전면허", "여권", "건강보험", "국세", "지방세", "세금", "보험", "공과", "청구서", "청첩장", "통장", "카드", "정부", "공공기관", "행정", "법원", "검찰", "경찰", "소송", "판결", "증인", "계약", "게약"],
    "02_AI_생성": ["ChatGPT", "Gemini", "DALL-E", "Generated", "AI"],
    "03_업무_프로젝트": ["GECKO", "공공근로", "팸플릿", "포스터", "poster", "사업자", "기획", "보고서", "발표", "회의"],
    "04_메신저": ["KakaoTalk", "LINE", "카톡", "라인", "photo_", "IMG_"],
    "05_금융_법률": ["은행", "복권", "행정소송", "법", "전세", "보험", "주식", "투자", "가계부"]
}

# 2. 확장자 기반 분류 규칙
EXTENSION_RULES = {
    "07_압축_파일": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "08_일반_문서[PDF]": [".pdf"],
    "09_일반_문서[텍스트]": [".txt"],
    "10_일반_문서[MS-Office]": [".docx", ".doc", ".xlsx", ".xls", ".csv", ".pptx", ".ppt"],
    "11_일반_문서[한컴]": [".hwp", ".hwpx"],
    "12_프로그램파일[C_언어]": [".h", ".c", ".cpp", ".cs"],
    "13_프로그램파일[HTML_관련]": [".html", ".css", ".js", ".php", ".json", ".xml"],
    "14_프로그램파일[파이썬_등]": [".py", ".ipynb"],
    "15_프로그램파일[기타]": [".java", ".class", ".sql", ".yaml", ".yml", ".md"],
    "16_시스템파일": [".ini", ".dll", ".msg", ".sys", ".tmp"],
    "17_실행파일": [".exe", ".bat", ".ps1", ".msi", ".msix"],
    "18_백업_및_기타": [".bak", ".old", ".log"]
}

# 3. 미디어 확장자 정의
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".heic", ".webp"]
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"]
DOCUMENT_EXTENSIONS = [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".hwp", ".hwpx", ".txt"]

# 4. 분석 및 스캔 설정 변수
# [스캔 범위 제어]
RECURSIVE_SCAN = True       # True: 하위 폴더까지 모두 뒤짐 / False: 현재 폴더만 정리

# [영상 분석]
MINUTES_PER_FRAME = 10      # 몇 분당 1장의 사진을 추출할지
MAX_FRAMES_PER_VIDEO = 20   # 한 영상당 최대 추출 장수

# [문서 분석]
MAX_DOC_TEXT_LENGTH = 5000  # 문서에서 읽어들일 최대 글자 수
FUZZY_MATCH_THRESHOLD = 80  # 키워드 유사도 매칭 임계값
