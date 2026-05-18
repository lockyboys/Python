# [3. 메인 실행 파일: organize_master_v7.py]
# 다른 파일(config, utils)들을 불러와서(import) 실제로 실행하는 컨트롤 타워입니다.

import config  # config.py 파일의 설정을 불러옵니다.
import utils   # utils.py 파일의 함수를 불러옵니다.

def run_organizer(target_path):
    target = utils.check_path_valid(target_path)
    if not target: return

    print(f"🚀 '{target_path}' 정리를 시작합니다 (모듈화 버전)...\n")
    count = 0

    for item in target.iterdir():
        # 폴더나 자기 자신(스크립트들)은 건너뜁니다.
        if item.is_dir() or item.name.startswith("organize_") or item.name in ["config.py", "utils.py"]:
            continue
        
        filename = item.name
        extension = item.suffix.lower()
        moved = False

        # 1. 키워드 기반 분석 (config.KEYWORD_RULES 사용)
        for folder, keywords in config.KEYWORD_RULES.items():
            if any(kw in filename for kw in keywords):
                utils.move_file_safely(item, target / folder)
                moved = True
                break
        
        if moved:
            count += 1
            continue

        # 2. 확장자 기반 분석 (config.EXTENSION_RULES 사용)
        for folder, exts in config.EXTENSION_RULES.items():
            if extension in exts:
                utils.move_file_safely(item, target / folder)
                moved = True
                break
        
        if moved:
            count += 1
            continue

        # 3. 일반 이미지 처리
        if extension in config.IMAGE_EXTENSIONS:
            utils.move_file_safely(item, target / "09_일반_사진")
            moved = True
            count += 1
            continue

        # 4. 기타
        utils.move_file_safely(item, target / "10_기타_파일")
        count += 1

    print(f"\n✨ 총 {count}개의 파일 정리가 완료되었습니다!")

if __name__ == "__main__":
    path = input("정리할 폴더 경로를 입력하세요: ").strip()
    run_organizer(path)
