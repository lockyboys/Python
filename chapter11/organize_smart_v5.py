import os
import shutil
from pathlib import Path

def organize_smart_v5(target_path):
    target = Path(target_path)
    if not target.exists():
        print(f"Error: {target_path} 경로를 찾을 수 없습니다.")
        return

    # 키워드 기반 분류 규칙 정의
    rules = {
        "Important_Documents": ["계약서", "신분증", "등록증", "확인서", "통지서", "등본", "신고필증", "검진확인서"],
        "AI_Generated": ["ChatGPT", "Gemini", "DALL-E", "Generated"],
        "Messenger": ["KakaoTalk", "LINE", "카톡"],
        "Work_Project": ["GECKO", "공공근로", "팸플릿", "포스터", "poster"],
        "Legal_Admin": ["행정소송", "법", "조항"],
        "Personal_Finance": ["주거래은행", "동행복권", "전세"]
    }

    # 기본 확장자 분류
    extensions = {
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Archives": [".zip", ".rar", ".7z"],
        "Executables": [".exe", ".msi"]
    }

    print("🚀 파일명 분석 및 지능형 정리를 시작합니다...")

    for item in target.iterdir():
        if item.is_dir() or item.name == "organize_smart_v5.py":
            continue
        
        filename = item.name
        extension = item.suffix.lower()
        moved = False

        # 1. 파일명 키워드 우선 분석 (이미지 및 문서 공통)
        for folder_name, keywords in rules.items():
            if any(kw in filename for kw in keywords):
                dest_dir = target / folder_name
                dest_dir.mkdir(exist_ok=True)
                shutil.move(str(item), str(dest_dir / filename))
                print(f"🔍 [키워드 매칭] {filename} -> {folder_name}/")
                moved = True
                break
        
        if moved: continue

        # 2. 확장자 기반 기본 분류
        for folder_name, exts in extensions.items():
            if extension in exts:
                dest_dir = target / folder_name
                dest_dir.mkdir(exist_ok=True)
                shutil.move(str(item), str(dest_dir / filename))
                print(f"📁 [확장자 분류] {filename} -> {folder_name}/")
                moved = True
                break
        
        if moved: continue

        # 3. 남은 이미지 파일 처리
        if extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
            dest_dir = target / "General_Images"
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_dir / filename))
            print(f"🖼️ [일반 이미지] {filename} -> General_Images/")
            moved = True

        # 4. 기타 파일
        if not moved:
            dest_dir = target / "Others"
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_dir / filename))
            print(f"❓ [기타] {filename} -> Others/")

    print("\n✨ 지능형 정리가 모두 완료되었습니다!")

if __name__ == "__main__":
    print("=== 키워드 기반 지능형 정리 도구 (v5) ===")
    path = input("정리할 폴더 경로를 입력하세요: ").strip()
    organize_smart_v5(path)
