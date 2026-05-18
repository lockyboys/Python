import os
import shutil
from pathlib import Path

def organize_folder(target_path):
    # 대상 경로가 존재하는지 확인
    target = Path(target_path)
    if not target.exists():
        print(f"Error: {target_path} 경로를 찾을 수 없습니다.")
        return

    # 분류할 폴더 정의
    folders = {
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".hwp"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Executables": [".exe", ".msi", ".sh", ".bat"]
    }

    # 분류 폴더 생성
    for folder_name in folders.keys():
        (target / folder_name).mkdir(exist_ok=True)
    
    # 기타 파일을 위한 폴더
    (target / "Others").mkdir(exist_ok=True)

    # 파일 분류 및 이동
    for item in target.iterdir():
        # 폴더는 건너뜀 (이미 생성한 분류 폴더 제외)
        if item.is_dir():
            continue
        
        # 파일 확장자 확인
        moved = False
        extension = item.suffix.lower()
        
        for folder_name, extensions in folders.items():
            if extension in extensions:
                dest = target / folder_name / item.name
                shutil.move(str(item), str(dest))
                print(f"Moved: {item.name} -> {folder_name}/")
                moved = True
                break
        
        # 분류되지 않은 파일 이동 (스크립트 파일 자체는 제외)
        if not moved and item.name != "organize_drive.py":
            dest = target / "Others" / item.name
            shutil.move(str(item), str(dest))
            print(f"Moved: {item.name} -> Others/")

    # 빈 폴더 삭제 (옵션)
    for item in target.iterdir():
        if item.is_dir() and not any(item.iterdir()):
            if item.name not in folders.keys() and item.name != "Others":
                item.rmdir()
                print(f"Removed empty folder: {item.name}")

if __name__ == "__main__":
    # 사용자가 원하는 경로 입력 (예: 'D:/Downloads' 또는 '/home/ubuntu/test')
    path_to_organize = input("정리할 폴더의 전체 경로를 입력하세요: ")
    organize_folder(path_to_organize)
    print("정리가 완료되었습니다!")
