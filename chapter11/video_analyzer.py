# [video_analyzer.py] - 영상 분석 모듈 (v15 - Robust Error Handling)
import os
import cv2
from pathlib import Path
from datetime import datetime, timedelta
import config
import utils
import image_analyzer
from collections import Counter
import utils

EXCLUDE_LIST = [
    "AI_TF_분석결과",
    "logs",
    "temp",
    "$RECYCLE.BIN",
    "System Volume Information"
]
# -----------------------------------------
# 영상 분석 및 그룹화 모듈
# [개선] 영상 분석 및 그룹화 모듈 개선하여 영상 분석 시 프레임 추출 간격, 한 영상당 최대 추출 장수 등을 설정할 수 있도록 개선
# [개선] 영상 분석 및 그룹화 모듈 개선하여 분석 실패 시에도 기본 분류로 이동하도록 보완
# [개선] 영상 분석 및 그룹화 모듈 개선하여 분석 과정에서 제외 폴더 내 파일 보호 로직 추가 (해체 모드가 아닐 때)
# [개선] 영상 분석 및 그룹화 모�듈 개선하여 분석 중 발생하는 오류는 로그에 기록하되, 시스템이 계속 작동하도록 예외 처리 강화
# -----------------------------------------
# def group_videos(target_path):
#     # --------------------------------
#     # AI 결과 루트
#     # --------------------------------
#     result_root = utils.get_ai_result_root( target_path )
#     target = Path(target_path)
#     videos = []
    
#     try:
#         #search_pattern = '**/*' if config.RECURSIVE_SCAN else '*'
#         #for f in target.glob(search_pattern):
#         all_files = utils.get_initial_files()

#         # for f in all_files:
#         #     if f.is_file() and f.suffix.lower() in config.VIDEO_EXTENSIONS:
#         #         if any(p.name.startswith(('0', '영상_그룹')) for p in f.parents if p != target):
#         #             continue
#         #         videos.append({'path': f, 'time': datetime.fromtimestamp(f.stat().st_mtime)})
#         all_files = utils.get_initial_files()

#         for f in all_files:

#             if f.suffix.lower() not in ( config.VIDEO_EXTENSIONS ):
#                 continue

#         target = result_root / "07_영상"

#         utils.move_file(f, target)
#         if not videos: return 0
#         videos.sort(key=lambda x: x['time'])

#         count = 0
#         current_group = [videos[0]]
#         for i in range(1, len(videos)):
#             if (videos[i]['time'] - videos[i-1]['time']) < timedelta(hours=4):
#                 current_group.append(videos[i])
#             else:
#                 count += _process_video_group(target, current_group)
#                 current_group = [videos[i]]
#         count += _process_video_group(target, current_group)
#         return count
#     except Exception as e:
#         utils.log_error(f"영상 그룹화 프로세스 오류: {e}")
#         return 0
def group_videos(target_path):
    # --------------------------------
    # AI 결과 루트
    # --------------------------------
    result_root = utils.get_ai_result_root( target_path )
    base_path = Path(target_path)
    # --------------------------------
    # 일반 영상 결과 폴더
    # --------------------------------
    video_root = ( base_path / "07_영상" )
    videos = []
    try:
        # --------------------------------
        # 최초 상태 파일만 탐색
        # --------------------------------
        all_files = utils.get_initial_files()
        for f in all_files:
            try:
                # 파일만 처리
                if not f.is_file():
                    continue
                # 영상 확장자 검사
                if ( f.suffix.lower()  not in config.VIDEO_EXTENSIONS ):
                    continue
                # # 결과 폴더 제외
                # if any( p.name.startswith( config.SKIP_FOLDERS ) for p in f.parents ):
                #     continue
                # --------------------------------
                # 결과 폴더 제외
                # --------------------------------
                if any( p.name.startswith(config.SKIP_FOLDERS)  for p in f.parents if p != base_path ):
                    continue
                    # --------------------------------
                    # 전체 해체 모드면
                    # 기존 영상 폴더는 허용
                    # --------------------------------
                    if config.UNPACK_ALL:
                        # AI 결과 폴더만 제외
                        if any( p.name == config.AI_RESULT_DIR for p in f.parents ):
                            continue
                    else:
                        continue
                videos.append({ 'path': f, 'time': datetime.fromtimestamp( f.stat().st_mtime ) })
            except Exception as e:
                utils.log_error( f"영상 정보 분석 실패 ({f}): {e}" )
        # 영상 없으면 종료
        if not videos:
            return 0
        # --------------------------------
        # 시간순 정렬
        # --------------------------------
        videos.sort( key=lambda x: x['time'] )
        count = 0
        current_group = [videos[0]]
        # --------------------------------
        # 시간 기준 그룹화
        # --------------------------------
        for i in range(1, len(videos)):
            time_diff = ( videos[i]['time'] - videos[i - 1]['time'] )
            # 4시간 이내면 같은 그룹
            if time_diff < timedelta(hours=4):
                current_group.append( videos[i] )
            else:
                count += _process_video_group( video_root, current_group )
                current_group = [videos[i]]
        # --------------------------------
        # 마지막 그룹 처리
        # --------------------------------
        count += _process_video_group( video_root, current_group )
        return count
    except Exception as e:
        utils.log_error( f"영상 그룹화 프로세스 오류: {e}" )
        return 0

# -----------------------------------------
# 영상 그룹 처리 함수
# [개선] 영상 그룹 처리 함수 개선하여 분석된 카테고리를 기반으로 그룹 폴더 이름을 생성하도록 개선
# [개선] 영상 그룹 처리 함수 개선하여 분석된 카테고리가 없는 경우 기본적으로 '일반영상'으로 분류하도록 개선
# [개선] 영상 그룹 처리 함수 개선하여 분석된 카테고리에 날짜/시간 패턴이 포함된 경우, 패턴을 제거하고 카테고리명만 폴더 이름에 포함하도록 개선
# [개선] 영상 그룹 처리 함수 개선하여 분석된 카테고리가 이미 'Group_'으로 시작하는 경우는 원래 분류된 폴더로 간주하여 마킹에서 제외하도록 개선
# [개선] 영상 그룹 처리 함수 개선하여 그룹 처리 중 오류 발생 시 상세 오류 메시지 출력 및 로그 기록 강화
# -----------------------------------------
def _process_video_group(target, group):
    try:
        all_categories = []
        for v in group:
            categories = _analyze_video_multi_frames(v['path'])
            all_categories.extend(categories)
        
        if all_categories:
            most_common = Counter(all_categories).most_common(1)[0][0]
            analysis_result = most_common
        else:
            analysis_result = "일반영상"
        
        if "_" in analysis_result and analysis_result[:2].isdigit():
            analysis_result = analysis_result.split("_", 1)[1]
        
        folder_name = f"Group_{group[0]['time'].strftime('%Y%m%d_%H%M')}_{analysis_result}"
        dest_dir = target / "06_영상_그룹" / folder_name
        
        for v in group:
            utils.move_file(v['path'], dest_dir)
        return len(group)
    except Exception as e:
        utils.log_error(f"영상 그룹 처리 오류: {e}")
        return 0
# -----------------------------------------
# 영상 개별 분석 함수
# [개선] 영상 개별 분석 함수 개선하여 영상에서 여러 프레임을 추출하여 분석하도록 개선
# [개선] 영상 개별 분석 함수 개선하여 분석된 카테고리를 리스트로 반환하도록 개선
# [개선] 영상 개별 분석 함수 개선하여 분석 중 발생하는 오류는 로그에 기록하되, 시스템이 계속 작동   하도록 예외 처리 강화
# -----------------------------------------
def _analyze_video_multi_frames(video_path):
    categories = []
    try:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened(): return []
            
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = total_frames / fps if fps > 0 else 0
        
        interval_sec = config.MINUTES_PER_FRAME * 60
        num_frames = min(int(duration_sec / interval_sec) + 1, config.MAX_FRAMES_PER_VIDEO)
        if num_frames == 0: num_frames = 1
            
        print(f"🎬 영상 분석: {video_path.name} ({num_frames}개 프레임)")
        
        for i in range(num_frames):
            target_frame = int((total_frames / num_frames) * i + (total_frames / (num_frames * 2))) if num_frames > 1 else total_frames // 2
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ret, frame = cap.read()
            
            if ret:
                temp_path = Path(f"temp_v_{i}.jpg")
                cv2.imwrite(str(temp_path), frame)
                categories.append(image_analyzer.analyze_image_final(temp_path))
                if temp_path.exists(): temp_path.unlink()
        cap.release()
    except Exception as e:
        utils.log_error(f"영상 개별 분석 오류 ({video_path.name}): {e}")
    return categories
