from pathlib import Path

APP_NAME = "Smart File Organizer"
CURRENT_PROJECT_DIR = Path(__file__).parent.absolute()

# 로그 파일 생성 방식입니다. 실행 대상 폴더 아래의 Logs 폴더로 변경됩니다.
LOG_FILE_YN = True
LOG_DATE_YN = True
BASE_LOG_DIR = str(CURRENT_PROJECT_DIR / "Logs")
LOG_FILE_PREFIX = "organizer_log"
LOG_FILE_NAME = None

# 정리 결과와 원본 격리 폴더 이름입니다.
RESULT_FOLDER_NAME = "50_AI_분석결과"
ISOLATION_FOLDER_NAME = "00_원본_격리보관"

# True면 하위 폴더 안의 파일을 먼저 원본 격리 폴더로 모읍니다.
UNPACK_ALL = True
SHOW_PROGRESS = True

# 실수로 시스템 폴더를 정리하지 않도록 막는 보호 키워드입니다.
SYSTEM_PROTECTED_KEYWORDS = [
    "c:\\windows",
    "c:\\source",
    "c:\\program files",
    "c:\\program files (x86)",
    "c:\\programdata",
    "c:\\users\\all users",
]

VIDEO_EXTENSIONS = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"]
DOCUMENT_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".doc",
    ".dot",
    ".dotx",
    ".dotm",
    ".xlsx",
    ".xls",
    ".xlsm",
    ".xlt",
    ".xltx",
    ".xltm",
    ".pptx",
    ".ppt",
    ".pptm",
    ".pps",
    ".ppsx",
    ".ppsm",
    ".pot",
    ".potx",
    ".potm",
    ".hwp",
    ".hwpx",
    ".hml",
    ".rtf",
    ".odt",
    ".ods",
    ".odp",
    ".txt",
    ".csv",
    ".md",
]
IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp", ".heic"]
AUDIO_EXTENSIONS = [".mp3", ".wav", ".flac", ".ogg", ".wma", ".m4a", ".aac"]

# 프로그램이 미리 만들어 두는 분류 폴더 이름입니다.
DOC_FOLDER = "01_중요문서_및_행정"
VIDEO_FOLDER = "04_메신저_및_영상"
NATURE_IMAGE_FOLDER = "07_AI_자연_및_국내외풍경"
CITY_IMAGE_FOLDER = "08_AI_도시_랜드마크_및_건축물"
PEOPLE_IMAGE_FOLDER = "09_AI_인물_및_일상_오류"
AUDIO_FOLDER = "10_오디오_음성"
OTHER_FOLDER = "98_미분류_기타"

PRE_BUILD_FOLDERS = [
    DOC_FOLDER,
    VIDEO_FOLDER,
    NATURE_IMAGE_FOLDER,
    CITY_IMAGE_FOLDER,
    PEOPLE_IMAGE_FOLDER,
    AUDIO_FOLDER,
    OTHER_FOLDER,
]

PRE_BUILD_FILES = {
    DOC_FOLDER: [
        "중요문서_보안주의.txt",
        "문서정리_매뉴얼.txt",
    ],
    OTHER_FOLDER: [
        "미분류_확인필요.txt",
    ],
}

DEFAULT_DOC_FOLDER = DOC_FOLDER
DEFAULT_VIDEO_FOLDER = VIDEO_FOLDER
DEFAULT_IMAGE_FOLDER = PEOPLE_IMAGE_FOLDER
DEFAULT_AUDIO_FOLDER = AUDIO_FOLDER
DEFAULT_OTHER_FOLDER = OTHER_FOLDER
CORRUPTED_IMAGE_FOLDER = OTHER_FOLDER

EXCLUDE_LIST = {"Thumbs.db", "desktop.ini", "$RECYCLE.BIN"}

# 문서 파일명에 이 단어들이 있으면 중요 문서 폴더로 보냅니다.
KEYWORD_RULES = {
    DOC_FOLDER: [
        "매출",
        "계좌",
        "거래",
        "영수증",
        "계약",
        "보고",
        "증명",
        "세금",
        "invoice",
        "receipt",
        "contract",
        "report",
    ],
}

# 이미지 파일명에 들어간 단어로 자연/도시/인물 폴더를 고릅니다.
FILENAME_ROOM_RULES = {
    NATURE_IMAGE_FOLDER: [
        "풍경",
        "바다",
        "산",
        "하늘",
        "여행",
        "nature",
        "beach",
        "sea",
        "mountain",
        "trip",
        "travel",
    ],
    CITY_IMAGE_FOLDER: [
        "도시",
        "빌딩",
        "건축",
        "아파트",
        "타워",
        "city",
        "building",
        "tower",
        "street",
    ],
    PEOPLE_IMAGE_FOLDER: [
        "사람",
        "인물",
        "가족",
        "셀카",
        "일상",
        "face",
        "person",
        "selfie",
        "kakao",
    ],
}

# 파일 확장자만 보고 최종 폴더를 결정할 때 쓰는 기본 규칙입니다.
EXTENSION_RULES = {
    VIDEO_FOLDER: VIDEO_EXTENSIONS,
    DOC_FOLDER: DOCUMENT_EXTENSIONS,
    PEOPLE_IMAGE_FOLDER: IMAGE_EXTENSIONS,
    AUDIO_FOLDER: AUDIO_EXTENSIONS,
}
