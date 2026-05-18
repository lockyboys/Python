import os
import shutil
from pathlib import Path

"""
[폴더 정리 마스터 스크립트 v6]
이 스크립트는 파일의 '확장자'와 '파일명 키워드'를 모두 분석하여 지능적으로 파일을 분류합니다.
"""

def start_organizing(target_path):
    # 1. 경로 설정 및 유효성 검사
    target = Path(target_path)
    if not target.exists():
        print(f"❌ 오류: '{target_path}' 경로를 찾을 수 없습니다.")
        return

    # 2. 분류 규칙 정의 (파일명 키워드 기반)
    # 파일 이름에 아래 단어가 포함되어 있으면 해당 폴더로 우선 분류됩니다.
    keyword_rules = {
        "01_중요문서_및_증명서": ["신분증", "계약서", "등록증", "확인서", "통지서", "등본", "신고필증", "검진", "영수증"],
        "02_AI_생성_이미지": ["ChatGPT", "Gemini", "DALL-E", "Generated", "AI"],
        "03_업무_및_프로젝트": ["GECKO", "공공근로", "팸플릿", "포스터", "poster", "사업자"],
        "04_메신저_다운로드": ["KakaoTalk", "LINE", "카톡", "라인"],
        "05_금융_및_법률": ["은행", "복권", "행정소송", "법", "전세", "보험"]
    }

    # 3. 기본 확장자 분류 규칙
    extension_rules = {
        "06_영상_파일": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "07_압축_및_실행파일": [".zip", ".rar", ".7z", ".exe", ".msi"],
        "08_일반_문서": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".hwp"]
    }

    print(f"📂 대상 폴더: {target_path}")
    print("🚀 지능형 분석 및 정리를 시작합니다...\n")

    # 4. 파일 탐색 및 이동 로직
    count = 0
    for item in target.iterdir():
        # 폴더이거나 현재 실행 중인 스크립트 파일은 건너뜁니다.
        if item.is_dir() or item.name == "organize_master.py":
            continue
        
        filename = item.name
        extension = item.suffix.lower()
        moved = False

        # [단계 A] 파일명 키워드 분석 (가장 우선순위가 높음)
        for folder_name, keywords in keyword_rules.items():
            if any(kw in filename for kw in keywords):
                move_file(item, target / folder_name)
                moved = True
                break
        
        if moved: 
            count += 1
            continue

        # [단계 B] 확장자 기반 분류
        for folder_name, exts in extension_rules.items():
            if extension in exts:
                move_file(item, target / folder_name)
                moved = True
                break
        
        if moved:
            count += 1
            continue

        # [단계 C] 분류되지 않은 이미지 파일
        if extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".heic"]:
            move_file(item, target / "09_일반_사진")
            moved = True
            count += 1
            continue

        # [단계 D] 그 외 기타 파일
        move_file(item, target / "10_기타_파일")
        count += 1

    print(f"\n✨ 정리 완료! 총 {count}개의 파일이 새로운 위치로 이동되었습니다.")

def move_file(source_path, dest_dir):
    """파일을 안전하게 이동시키는 보조 함수"""
    dest_dir.mkdir(exist_ok=True)
    dest_path = dest_dir / source_path.name
    
    # 동일한 이름의 파일이 목적지에 있을 경우를 대비
    if dest_path.exists():
        new_name = f"{source_path.stem}_{int(os.path.getmtime(source_path))}{source_path.suffix}"
        dest_path = dest_dir / new_name
        
    shutil.move(str(source_path), str(dest_path))
    print(f"✅ 이동: {source_path.name} -> {dest_dir.name}/")

if __name__ == "__main__":
    print("========================================")
    print("   지능형 폴더 정리 마스터 (v6 Final)   ")
    print("========================================")
    path = input("정리할 폴더의 경로를 입력하세요: ").strip()
    start_organizing(path)
