# [config.py] - 전체 시스템 설정 파일 (v25 - Logging Control)

# 1. 경로 및 로그 설정
BASE_LOG_DIR = r"C:\source\Python"
LOG_FILE_PREFIX = "error_log"

# 2. 제어 변수 (사용자가 직접 변경 가능)
RECURSIVE_SCAN = True      # 하위 폴더까지 스캔할지 여부
UNPACK_ALL = False         # 하위 구조를 모두 해체할지 여부
SHOW_PROGRESS = True       # 화면(콘솔)에 파일 이동 과정을 실시간으로 출력할지 여부
EXCLUDE_LIST = [
    "System Volume Information", "$RECYCLE.BIN", ".git", ".vscode", 
    "main_organizer.py", "config.py", "utils.py", "video_analyzer.py", 
    "image_analyzer.py", "document_analyzer.py", "gpu_setup_guide.md", 
    "zlibwapi_fix_guide.md", "오피스 2016"
]

# 3. 키워드 기반 분류 규칙 (문서용)
KEYWORD_RULES = {
    "01_중요문서": ["신분증", "계약서", "등록증", "확인서", "통지서", "등본", "신고필증", "검진", "영수증", "명세서", "증명원", "증명서", "인감", "주민등록", "운전면허", "여권", "건강보험", "국세", "지방세", "세금", "보험", "공과", "청구서", "청첩장", "통장", "카드", "정부", "공공기관", "행정", "법원", "검찰", "경찰", "소송", "판결", "증인", "계약", "게약"],
    "02_AI_생성": ["ChatGPT", "Gemini", "DALL-E", "Generated", "AI"],
    "03_업무_프로젝트": ["GECKO", "공공근로", "팸플릿", "포스터", "poster", "사업자", "기획", "보고서", "발표", "회의"],
    "04_메신저": ["KakaoTalk", "LINE", "카톡", "라인"],
    "05_금융_법률": ["은행", "복권", "행정소송", "법", "전세", "보험", "주식", "투자", "가계부"]
}

# 4. 확장자 기반 분류 규칙
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

# 5. 미디어 확장자 정의
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".heic", ".webp"]
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"]
DOCUMENT_EXTENSIONS = [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".hwp", ".hwpx", ".txt"]

# 6. 분석 세부 설정
MINUTES_PER_FRAME = 10
MAX_FRAMES_PER_VIDEO = 20
MAX_DOC_TEXT_LENGTH = 5000
