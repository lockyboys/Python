# [video_analyzer.py] - 영상 분석 모듈 (v15 - Robust Error Handling)
import os
import cv2
import shutil
import utils

import config
import image_analyzer

from pathlib import Path
from datetime import datetime, timedelta
from collections import Counter
from pathlib import Path

def group_videos(target_path, video_files):

    target = Path(target_path)

    video_root = target / "06_영상_그룹"

    moved_count = 0

    for f in video_files:

        try:
            if utils.is_excluded(f):
                continue

            ext = f.suffix.lower()

            # 확장자별 폴더
            dest_dir = video_root / ext.replace('.', '').upper()

            utils.move_file(f, dest_dir)

            moved_count += 1

        except Exception as e:
            utils.log_error(
                f"영상 처리 오류 ({f.name}): {e}"
            )

    return moved_count

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
