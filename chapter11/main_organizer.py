# [main_organizer.py] - 전체 시스템 통합 실행 파일
import config
import utils
import video_analyzer  # 영상 분석 모듈 연결
import image_analyzer  # AI 이미지 분석 모듈 연결 (신규 추가!)
from pathlib import Path

def run_total_organization(path_str):
    # [안전 장치 1] 경로가 비어있거나 공백인 경우 차단
    if not path_str or not path_str.strip():
        print("\n⚠️ 알림: 정리할 폴더 경로가 입력되지 않았습니다.")
        print("프로그램을 안전하게 종료합니다.")
        return

    path = utils.validate_path(path_str)
    if not path:
        print(f"❌ 오류: '{path_str}' 경로를 찾을 수 없거나 유효하지 않습니다.")
        return

    # [안전 장치 2] 현재 스크립트가 실행 중인 폴더를 정리하려고 할 때 경고
    current_dir = Path.cwd().absolute()
    target_dir = path.absolute()
    if current_dir == target_dir:
        confirm = input(f"\n⚠️ 경고: 현재 스크립트가 있는 폴더({target_dir})를 정리하시겠습니까? (y/n): ")
        if confirm.lower() != 'y':
            print("작업을 취소합니다.")
            return

    target = utils.validate_path(path_str)
    if not target:
        print("❌ 유효하지 않은 경로입니다.")
        return

    print(f"🌟 통합 폴더 정리 시스템을 시작합니다: {path_str}\n")

    # 1. 영상 그룹화 (외부 모듈 호출)
    print("--- [단계 1] 영상 지능형 분석 및 그룹화 ---")
    v_count = video_analyzer.group_videos(target)

    # 2. AI 이미지 분석 (외부 모듈 호출)
    print("\n--- [단계 2] AI 이미지 내용 분석 및 분류 ---")
    i_count = image_analyzer.run_image_ai_organizing(target)
    
    # 2. 키워드 및 확장자 정리 (내부 로직 + 설정/유틸 연결)
    print("\n--- [단계 2] 파일명 키워드 및 확장자 기반 정리 ---")
    f_count = 0
    for item in target.iterdir():
        if item.is_dir() or item.name in ["main_organizer.py", "config.py", "utils.py", "video_analyzer.py"]:
            continue
        
        moved = False
        # 키워드 우선순위 정리
        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw in item.name for kw in kws):
                utils.move_file(item, target / folder)
                moved = True
                break
        
        if not moved:
            # 확장자 기반 정리
            for folder, exts in config.EXTENSION_RULES.items():
                if item.suffix.lower() in exts:
                    utils.move_file(item, target / folder)
                    moved = True
                    break
        
        if not moved and item.suffix.lower() in config.IMAGE_EXTENSIONS:
            utils.move_file(item, target / "09_일반_사진")
            moved = True

        if moved: f_count += 1

    print(f"\n✅ 전체 정리 완료! (영상: {v_count}개, AI 이미지: {i_count}개, 기타 파일: {f_count}개)")

if __name__ == "__main__":
    path = input("정리할 폴더 경로를 입력하세요: ").strip()
    run_total_organization(path)
