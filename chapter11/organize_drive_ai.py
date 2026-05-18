import os
import shutil
from pathlib import Path
import datetime

# 이미지 분석을 위한 라이브러리 (설치가 필요할 수 있음)
try:
    from PIL import Image
    from PIL.ExifTags import TAGS
except ImportError:
    print("알림: PIL(Pillow) 라이브러리가 없습니다. 사진 날짜 분석 기능이 제한될 수 있습니다.")

def get_image_date(file_path):
    """사진의 촬영 날짜를 추출합니다."""
    try:
        image = Image.open(file_path)
        info = image._getexif()
        if info:
            for tag, value in info.items():
                tag_name = TAGS.get(tag, tag)
                if tag_name == "DateTimeOriginal":
                    return datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    
    # EXIF 데이터가 없으면 파일 수정 날짜 사용
    timestamp = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(timestamp)

def organize_folder_ai(target_path):
    target = Path(target_path)
    if not target.exists():
        print(f"Error: {target_path} 경로를 찾을 수 없습니다.")
        return

    # 기본 분류 폴더
    categories = {
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".hwp"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Executables": [".exe", ".msi", ".sh", ".bat"],
        "Photos": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".heic"]
    }

    # 폴더 생성
    for cat in categories.keys():
        (target / cat).mkdir(exist_ok=True)
    (target / "Others").mkdir(exist_ok=True)

    print("🚀 AI 분석 및 정리를 시작합니다...")
    print("💡 팁: 이 스크립트는 사진의 촬영 날짜를 분석하여 연도-월별로 자동 분류합니다.")

    for item in target.iterdir():
        if item.is_dir() or item.name == "organize_drive_ai.py":
            continue
        
        extension = item.suffix.lower()
        moved = False

        # 1. 사진 세부 분류 (날짜별)
        if extension in categories["Photos"]:
            date = get_image_date(item)
            year_month = date.strftime("%Y-%m")
            photo_dir = target / "Photos" / year_month
            photo_dir.mkdir(parents=True, exist_ok=True)
            
            dest = photo_dir / item.name
            shutil.move(str(item), str(dest))
            print(f"📸 [사진 분류] {item.name} -> Photos/{year_month}/")
            moved = True

        # 2. 기타 파일 분류
        if not moved:
            for cat, exts in categories.items():
                if extension in exts:
                    dest = target / cat / item.name
                    shutil.move(str(item), str(dest))
                    print(f"📁 [{cat}] {item.name} -> {cat}/")
                    moved = True
                    break
        
        # 3. 분류되지 않은 파일
        if not moved:
            dest = target / "Others" / item.name
            shutil.move(str(item), str(dest))
            print(f"❓ [기타] {item.name} -> Others/")

    print("\n✨ 모든 정리가 완료되었습니다!")

if __name__ == "__main__":
    print("=== AI 기반 스마트 폴더 정리 도구 (v3) ===")
    path_to_organize = input("정리할 폴더 경로를 입력하세요: ").strip()
    organize_folder_ai(path_to_organize)
