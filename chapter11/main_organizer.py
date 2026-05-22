# [main_organizer.py] - 전체 시스템 통합 실행 파일 (v15 - Control & Full Logging)
import os
import sys
import config
import utils
import video_analyzer
import image_analyzer
import document_analyzer
from pathlib import Path

def check_gpu_status():
    print("🔍 하드웨어 가속 진단 중...")
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✅ NVIDIA GPU 감지됨: {len(gpus)}개 장치 사용 가능")
            return True
        else:
            print("ℹ️ NVIDIA GPU를 찾을 수 없습니다. CPU 모드로 작동합니다.")
            return False
    except Exception as e:
        utils.log_error(f"GPU 진단 오류: {e}")
        return False

def run_total_organization(path_str):
    try:
        path = utils.validate_path(path_str)
        if not path:
            print(f"❌ 오류: '{path_str}' 경로가 유효하지 않습니다.")
            return

        print(f"🌟 통합 폴더 정리 시스템(v15)을 시작합니다: {path_str}")
        print(f"📂 스캔 모드: {'하위 폴더 포함(Deep Scan)' if config.RECURSIVE_SCAN else '현재 폴더만(Quick Scan)'}")
        gpu_active = check_gpu_status()
        print("-" * 50)

        # 1. 영상 분석
        v_count = video_analyzer.group_videos(path)

        # 2. 문서 분석
        d_count = document_analyzer.run_document_organizing(path)

        # 3. 이미지 AI 분석
        i_count = image_analyzer.run_image_ai_organizing(path)
        
        # 4. 기타 파일 싹쓸이
        print("\n--- [단계 4] 기타 파일 싹쓸이 정리 ---")
        f_count = 0
        search_pattern = '**/*' if config.RECURSIVE_SCAN else '*'
        all_files = [f for f in path.glob(search_pattern) if f.is_file()]
        
        script_files = ["main_organizer.py", "config.py", "utils.py", "video_analyzer.py", "image_analyzer.py", "document_analyzer.py", "error_log.txt", "gpu_setup_guide.md", "zlibwapi_fix_guide.md"]
        
        for item in all_files:
            try:
                if item.name in script_files: continue
                if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹', 'Group_')) for p in item.parents if p != path):
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
                
                if not moved:
                    if item.suffix.lower() in config.IMAGE_EXTENSIONS:
                        utils.move_file(item, path / "09_일반_사진")
                    else:
                        utils.move_file(item, path / "99_미분류_기타")
                    moved = True
                if moved: f_count += 1
            except Exception as e:
                utils.log_error(f"파일 개별 처리 오류 ({item.name}): {e}")

        print(f"\n✅ 전체 정리 완료!")
        print(f"📊 통계: 영상 {v_count}개, 문서 {d_count}개, AI 이미지 {i_count}개, 기타 {f_count}개")
        if gpu_active: print("🚀 NVIDIA GPU 가속 엔진이 성공적으로 작동했습니다.")
        
    except Exception as e:
        utils.log_error(f"메인 프로세스 치명적 오류: {e}")
        print(f"❌ 치명적 오류 발생! 상세 내용은 error_log.txt를 확인하세요.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path_input = sys.argv[1]
    else:
        path_input = input("정리할 폴더 경로를 입력하세요: ").strip()
    run_total_organization(path_input)
