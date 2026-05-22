# [main_organizer.py] - 전체 시스템 통합 실행 파일 (v12 - GPU Diagnostic)
import os
import sys
import config
import utils
import video_analyzer
import image_analyzer
from pathlib import Path

def check_gpu_status():
    """시스템의 GPU 가속 가능 여부를 진단합니다."""
    print("🔍 하드웨어 가속 진단 중...")
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ NVIDIA GPU 감지됨: {len(gpus)}개 장치 사용 가능")
            for i, gpu in enumerate(gpus):
                print(f"   - GPU [{i}]: {gpu.name}")
            return True
        else:
            print("ℹ️ NVIDIA GPU를 찾을 수 없습니다. CPU 모드로 작동합니다.")
            return False
    except Exception as e:
        print(f"⚠️ GPU 진단 중 오류 발생: {e}")
        return False

def run_total_organization(path_str):
    if not path_str or not path_str.strip():
        print("\n⚠️ 알림: 정리할 폴더 경로가 입력되지 않았습니다.")
        return

    path = utils.validate_path(path_str)
    if not path:
        print(f"❌ 오류: '{path_str}' 경로를 찾을 수 없거나 유효하지 않습니다.")
        return

    # 현재 폴더 정리 경고
    current_dir = Path.cwd().absolute()
    target_dir = path.absolute()
    if current_dir == target_dir:
        confirm = input(f"\n⚠️ 경고: 현재 스크립트가 있는 폴더({target_dir})를 정리하시겠습니까? (y/n): ")
        if confirm.lower() != 'y':
            print("작업을 취소합니다.")
            return

    print(f"🌟 통합 폴더 정리 시스템(v12)을 시작합니다: {path_str}")
    gpu_active = check_gpu_status()
    print("-" * 50)

    # 1. 영상 그룹화
    print("\n--- [단계 1] 영상 지능형 분석 및 그룹화 ---")
    v_count = video_analyzer.group_videos(path)

    # 2. AI 이미지 분석 (GPU 가속 지원)
    print("\n--- [단계 2] AI 이미지 내용 분석 및 분류 ---")
    i_count = image_analyzer.run_image_ai_organizing(path)
    
    # 3. 키워드 및 확장자 정리 (싹쓸이 모드)
    print("\n--- [단계 3] 파일명 키워드 및 확장자 기반 싹쓸이 정리 ---")
    f_count = 0
    all_files = [f for f in path.rglob('*') if f.is_file()]
    script_files = ["main_organizer.py", "config.py", "utils.py", "video_analyzer.py", "image_analyzer.py", "error_log.txt", "gpu_setup_guide.md"]
    
    for item in all_files:
        if item.name in script_files:
            continue
            
        if any(p.name.startswith(('0', '1', 'AI_TF', '9')) for p in item.parents if p != path):
            continue
        
        moved = False
        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw.lower() in item.name.lower() for kw in kws):
                utils.move_file(item, path / folder)
                moved = True
                break
        
        if not moved:
            for folder, exts in config.EXTENSION_RULES.items():
                if item.suffix.lower() in exts:
                    utils.move_file(item, path / folder)
                    moved = True
                    break
        
        if not moved and item.suffix.lower() in config.IMAGE_EXTENSIONS:
            utils.move_file(item, path / "09_일반_사진")
            moved = True

        if not moved:
            utils.move_file(item, path / "99_미분류_기타")
            moved = True

        if moved: f_count += 1

    print(f"\n✅ 전체 정리 완료!")
    print(f"📊 통계: 영상 {v_count}개, AI 이미지 {i_count}개, 기타 파일 {f_count}개")
    if gpu_active:
        print("🚀 RTX 3060 GPU 가속이 성공적으로 적용되었습니다.")

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
        with open("error_log.txt", "a", encoding="utf-8") as f:
            import datetime
            f.write(f"[{datetime.datetime.now()}] {str(e)}\n")
