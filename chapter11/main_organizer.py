# [main_organizer.py] - 전체 시스템 통합 실행 파일 (v17 - Expert Fix)
import os
import sys
import config
import video_analyzer
import image_analyzer
import document_analyzer
from pathlib import Path


import utils
# -----------------------------------------
# 전체 시스템 통합 실행 파일
# [개선] 전체 시스템 통합 실행 파일 개선하여 각 단계별로 상세 로그 기록 및 오류 처리 강화
# [개선] 전체 시스템 통합 실행 파일 개선하여 시스템 상태 진단 및 보고 기능 추가
# [개선] 전체 시스템 통합 실행 파일 개선하여 사용자 입력 경로 검증 및 유효성 검사 강화
# [개선] 전체 시스템 통합 실행 파일 개선하여 각 단계별로 처리된 항목 수에 대한 통계 보고 기능 추가
# [개선] 전체 시스템 통합 실행 파일 개선하여 시스템 상태 진단 및 보고 기능 추가하여 시스템의 현재 상태와 각 단계별로 처리된 항목 수에 대한 상세 보고서 생성
# -----------------------------------------
def run_total_organization(path_str):
    try:
        path = utils.validate_path(path_str)

        if not path:
            print(f"❌ 오류: '{path_str}' 경로가 유효하지 않습니다.")
            return

        # -----------------------------------------
        # 프로그램 시작 당시 상태 기억
        # -----------------------------------------
        config.initial_folders, config.initial_files = ( utils.build_initial_state(path) )

        # 최초 폴더 구조 기억
        initial_folders = utils.build_initial_folder_set(path)

        # 1. 시스템 정밀 진단 및 로그 기록
        utils.get_system_status()
        
        print(f"\n📂 정리 대상: {path_str}")
        if config.UNPACK_ALL:
            print("⚠️ [해체 모드 활성화] 모든 하위 폴더의 파일을 루트로 모아 재분류합니다.")



        # 2. 영상 분석 및 그룹화
        print("\n--- [단계 1] 영상 지능형 분석 및 그룹화 ---")
        utils.log_message("단계 1: 영상 지능형 분석 및 그룹화 시작", "INFO")
        v_count = video_analyzer.group_videos(path, config.initial_folders, config.initial_files)

        # 3. 문서 분석 및 분류
        print("\n--- [단계 2] 문서 지능형 내용 분석 및 분류 ---")
        utils.log_message("단계 2: 문서 지능형 내용 분석 및 분류 시작", "INFO")
        d_count = document_analyzer.run_document_organizing(path, config.initial_folders, config.initial_files)

        # 4. 이미지 AI 분석 및 분류
        print("\n--- [단계 3] AI 이미지 내용 분석 및 분류 ---")
        utils.log_message("단계 3: AI 이미지 내용 분석 및 분류 시작", "INFO")
        i_count = image_analyzer.run_image_ai_organizing(path, config.initial_folders, config.initial_files)
        
        # 5. 기타 파일 싹쓸이 정리
        print("\n--- [단계 4] 기타 파일 싹쓸이 및 정리 ---")
        utils.log_message("단계 4: 기타 파일 싹쓸이 및 정리 시작", "INFO")
        f_count = 0
        #pattern = '**/*' if (config.RECURSIVE_SCAN or config.UNPACK_ALL) else '*'
        #all_files = [f for f in path.glob(pattern) if f.is_file()]
        all_files = utils.get_initial_files( config.initial_folders, config.initial_files )
        
        for item in all_files:
            try:

                # # 🔥 AI 분석 완료 폴더 보호
                # if "AI_TF_분석결과" in str(item):
                #     continue

                # 🔥 AI 분석 완료 폴더 보호
                if any(p.name == "AI_TF_분석결과" for p in item.parents):
                    continue

                # [개선] 경로 전체를 체크하여 제외 폴더 내 파일 보호
                if utils.is_excluded(item):
                    continue

                # 제외 리스트 확인
                if item.name in config.EXCLUDE_LIST or any(ex in str(item) for ex in config.EXCLUDE_LIST):
                    continue
                
                # 이미 분류된 폴더 제외 (해체 모드가 아닐 때)
                if not config.UNPACK_ALL:
                    if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹', 'Group_')) for p in item.parents if p != path):
                        continue
                
                moved = False
                # 1) 키워드 규칙
                for folder, kws in config.KEYWORD_RULES.items():
                    if any(kw.lower() in item.name.lower() for kw in kws):
                        utils.move_file(item, path / folder)
                        moved = True
                        break
                
                # 2) 확장자 규칙
                if not moved:
                    for folder, exts in config.EXTENSION_RULES.items():
                        if item.suffix.lower() in exts:
                            utils.move_file(item, path / folder)
                            moved = True
                            break
                
                # 3) 기본 분류
                if not moved:
                    if item.suffix.lower() in config.IMAGE_EXTENSIONS:
                        utils.move_file(item, path / "09_일반_사진")
                    else:
                        utils.move_file(item, path / "99_미분류_기타")
                    moved = True
                if moved: f_count += 1
            except Exception as e:
                utils.log_error(f"파일 처리 중 오류 ({item.name}): {e}")

        # 6. 빈 폴더 사후 관리
        print("\n--- [단계 5] 빈 폴더 사후 관리 ---")
        utils.log_message("단계 5: 빈 폴더 사후 관리 시작", "INFO")
        utils.mark_empty_folders(path)

        print(f"\n✅ 전체 정리 완료!")
        print(f"📊 통계: 영상 {v_count}개, 문서 {d_count}개, AI 이미지 {i_count}개, 기타 {f_count}개")
        print(f"📝 상세 진단 및 오류 로그는 '{utils._current_log_file}'를 확인하세요.")
        utils.log_message(f"\n✅전체 정리 완료: 영상 {v_count}개, 문서 {d_count}개, AI 이미지 {i_count}개, 기타 {f_count}개", "INFO")
    except Exception as e:
        utils.log_error(f"메인 프로세스 치명적 오류: {e}")
        print(f"❌ 치명적 오류 발생! 상세 내용은 로그를 확인하세요.")
# -----------------------------------------
# 메인 실행
# [개선] 메인 실행 개선하여 사용자 입력 경로 검증 및 유효성 검사 강화
# [개선] 메인 실행 개선하여 시스템 상태 진단 및 보고 기능 추가하여 시스템의 현재 상태와 각 단계별로 처리된 항목 수에 대한 상세 보고서 생성
#-----------------------------------------
if __name__ == "__main__":
    path_input = sys.argv[1] if len(sys.argv) > 1 else input("정리할 폴더 경로를 입력하세요: ").strip()
    run_total_organization(path_input)
