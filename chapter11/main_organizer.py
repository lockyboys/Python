# [main_organizer.py] - 속도 최적화 버전
import sys

import config
import utils
import image_analyzer
import video_analyzer
import document_analyzer


def run_total_organization(path_str):

    try:

        path = utils.validate_path(path_str)
        
        # 로그 파일 경로 생성
        config.CURRENT_LOG_FILE = utils.get_log_file()

        if not path:
            return

        utils.get_system_status()

        pattern = ( '**/*' if config.RECURSIVE_SCAN else '*' )

        utils.log_message("파일 목록 읽는 중...")

        all_files = [ f for f in path.glob(pattern) if f.is_file() ]

        utils.log_message( f"전체 파일 수: {len(all_files)}" )

        image_files = []
        video_files = []
        doc_files = []

        for f in all_files:

            if utils.is_excluded(f):
                continue

            ext = f.suffix.lower()

            if ext in config.IMAGE_EXTENSIONS:
                image_files.append(f)

            elif ext in config.VIDEO_EXTENSIONS:
                video_files.append(f)

            elif ext in config.DOCUMENT_EXTENSIONS:
                doc_files.append(f)

        utils.log_message( f"이미지={len(image_files)} " f"영상={len(video_files)} " f"문서={len(doc_files)}" )

        i_count = image_analyzer.run_image_ai_organizing( path, image_files )

        v_count = video_analyzer.group_videos( path, video_files )

        d_count = document_analyzer.run_document_organizing( path, doc_files )

        summary = ( f"✅ 전체 완료\n" f"이미지 {i_count}개 / " f"영상 {v_count}개 / " f"문서 {d_count}개" )

        utils.log_message(summary)

    except Exception as e:

        utils.log_error( f"메인 오류: {e}" )

if __name__ == "__main__":
    path_input = sys.argv[1] if len(sys.argv) > 1 else input("정리할 폴더 경로를 입력하세요: ").strip()
    run_total_organization(path_input)