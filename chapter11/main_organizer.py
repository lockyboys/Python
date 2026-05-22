# [main_organizer.py] - 전체 시스템 통합 실행 파일 (v24 - Image First)
import os
import sys
import config
import utils
import video_analyzer
import image_analyzer
import document_analyzer
from pathlib import Path

def run_total_organization(path_str):
    try:
        path = utils.validate_path(path_str)
        if not path:
            print(f"❌ 오류: '{path_str}' 경로가 유효하지 않습니다.")
            return

        utils.get_system_status()
        print(f"\n📂 정리 대상: {path_str}")

        # [단계 1] 이미지 분석 (가장 먼저 실행하여 AI 분류 정밀도 확보)
        print("\n--- [단계 1] AI 이미지 정밀 내용 분석 및 분류 ---")
        i_count = image_analyzer.run_image_ai_organizing(path)

        # [단계 2] 영상 분석
        print("\n--- [단계 2] 영상 지능형 분석 및 그룹화 ---")
        v_count = video_analyzer.group_videos(path)

        # [단계 3] 문서 분석
        print("\n--- [단계 3] 문서 지능형 내용 분석 및 분류 ---")
        d_count = document_analyzer.run_document_organizing(path)
        
        # [단계 4] 기타 파일 싹쓸이
        print("\n--- [단계 4] 기타 파일 싹쓸이 및 정리 ---")
        f_count = 0
        pattern = '**/*' if (config.RECURSIVE_SCAN or config.UNPACK_ALL) else '*'
        all_files = [f for f in path.glob(pattern) if f.is_file()]
        
        for item in all_files:
            try:
                if utils.is_excluded(item): continue
                
                if not config.UNPACK_ALL:
                    if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹')) for p in item.parents if p != path):
                        continue
                
                moved = False
                # 키워드 규칙 적용
                for folder, kws in config.KEYWORD_RULES.items():
                    if any(kw.lower() in item.name.lower() for kw in kws):
                        utils.move_file(item, path / folder)
                        moved = True
                        break
                
                # 확장자 규칙 적용
                if not moved:
                    for folder, exts in config.EXTENSION_RULES.items():
                        if item.suffix.lower() in exts:
                            utils.move_file(item, path / folder)
                            moved = True
                            break
                
                # 최종 미분류 처리
                if not moved:
                    if item.suffix.lower() in config.IMAGE_EXTENSIONS:
                        utils.move_file(item, path / "AI_TF_분석결과" / "09_일반_사진")
                    else:
                        utils.move_file(item, path / "99_미분류_기타")
                    moved = True
                if moved: f_count += 1
            except Exception as e:
                utils.log_error(f"파일 처리 오류 ({item.name}): {e}")

        # [단계 5] 빈 폴더 관리
        print("\n--- [단계 5] 빈 폴더 사후 관리 ---")
        utils.mark_empty_folders(path)

        print(f"\n✅ 전체 정리 완료!")
        print(f"📊 통계: 이미지 {i_count}개, 영상 {v_count}개, 문서 {d_count}개, 기타 {f_count}개")
        print(f"📝 상세 로그는 '{utils.get_log_path()}'를 확인하세요.")
        
    except Exception as e:
        utils.log_error(f"메인 프로세스 치명적 오류: {e}")
        print(f"❌ 치명적 오류 발생! 로그를 확인하세요.")

if __name__ == "__main__":
    path_input = sys.argv[1] if len(sys.argv) > 1 else input("정리할 폴더 경로를 입력하세요: ").strip()
    run_total_organization(path_input)
