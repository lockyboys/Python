# [main_organizer.py] - 전체 시스템 통합 실행 파일 (v10)
import os
import sys
import config
import utils
import video_analyzer  # 영상 분석 모듈 연결
import image_analyzer  # AI 이미지 분석 모듈 연결
from pathlib import Path

def run_total_organization(path_str):
    # [안전 장치 1] 경로 검증
    if not path_str or not path_str.strip():
        print("\n⚠️ 알림: 정리할 폴더 경로가 입력되지 않았습니다.")
        return

    path = utils.validate_path(path_str)
    if not path:
        print(f"❌ 오류: '{path_str}' 경로를 찾을 수 없거나 유효하지 않습니다.")
        return

    # [안전 장치 2] 현재 폴더 정리 경고
    current_dir = Path.cwd().absolute()
    target_dir = path.absolute()
    if current_dir == target_dir:
        confirm = input(f"\n⚠️ 경고: 현재 스크립트가 있는 폴더({target_dir})를 정리하시겠습니까? (y/n): ")
        if confirm.lower() != 'y':
            print("작업을 취소합니다.")
            return

    print(f"🌟 통합 폴더 정리 시스템(v10)을 시작합니다: {path_str}\n")

    # 1. 영상 그룹화 (하위 폴더 포함)
    print("--- [단계 1] 영상 지능형 분석 및 그룹화 ---")
    v_count = video_analyzer.group_videos(path)

    # 2. AI 이미지 분석 (OCR + TensorFlow)
    print("\n--- [단계 2] AI 이미지 내용 분석 및 분류 ---")
    i_count = image_analyzer.run_image_ai_organizing(path)
    
    # 3. 키워드 및 확장자 정리 (싹쓸이 모드)
    print("\n--- [단계 3] 파일명 키워드 및 확장자 기반 싹쓸이 정리 ---")
    f_count = 0
    
    # rglob('*')를 사용하여 모든 하위 파일 탐색
    all_files = [f for f in path.rglob('*') if f.is_file()]
    
    # 시스템 파일 제외
    script_files = ["main_organizer.py", "config.py", "utils.py", "video_analyzer.py", "image_analyzer.py", "error_log.txt"]
    
    for item in all_files:
        if item.name in script_files:
            continue
            
        # 이미 분류된 폴더 안에 있는 경우 제외 (01~99 또는 AI_TF로 시작하는 폴더)
        if any(p.name.startswith(('0', '1', 'AI_TF', '9')) for p in item.parents if p != path):
            continue
        
        moved = False
        # 키워드 우선순위 정리
        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw.lower() in item.name.lower() for kw in kws):
                utils.move_file(item, path / folder)
                moved = True
                break
        
        if not moved:
            # 확장자 기반 정리
            for folder, exts in config.EXTENSION_RULES.items():
                if item.suffix.lower() in exts:
                    utils.move_file(item, path / folder)
                    moved = True
                    break
        
        # 남은 이미지 처리
        if not moved and item.suffix.lower() in config.IMAGE_EXTENSIONS:
            utils.move_file(item, path / "09_일반_사진")
            moved = True

        # 끝까지 분류 안 된 파일
        if not moved:
            utils.move_file(item, path / "99_미분류_기타")
            moved = True

        if moved: f_count += 1

    print(f"\n✅ 전체 정리 완료! (영상: {v_count}개, AI 이미지: {i_count}개, 기타 파일: {f_count}개)")

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            path_input = sys.argv[1]
        else:
            path_input = input("정리할 폴더 경로를 입력하세요: ").strip()
        run_total_organization(path_input)
    except KeyboardInterrupt:
        print("\n사용자에 의해 작업이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류 발생: {e}")
        # utils.log_error(str(e)) # utils에 log_error가 없을 수도 있으므로 직접 기록
        with open("error_log.txt", "a", encoding="utf-8") as f:
            import datetime
            f.write(f"[{datetime.datetime.now()}] {str(e)}\n")
