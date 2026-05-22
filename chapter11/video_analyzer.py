# [video_analyzer.py] - 영상 분석 모듈 (v15 - Robust Error Handling)
import os
import cv2
from pathlib import Path
from datetime import datetime, timedelta
import config
import utils
import image_analyzer
from collections import Counter

def group_videos(target_path):
    target = Path(target_path)
    videos = []
    
    try:
        search_pattern = '**/*' if config.RECURSIVE_SCAN else '*'
        for f in target.glob(search_pattern):
            if f.is_file() and f.suffix.lower() in config.VIDEO_EXTENSIONS:
                if any(p.name.startswith(('0', '영상_그룹')) for p in f.parents if p != target):
                    continue
                videos.append({'path': f, 'time': datetime.fromtimestamp(f.stat().st_mtime)})
        
        if not videos: return 0
        videos.sort(key=lambda x: x['time'])

        count = 0
        current_group = [videos[0]]
        for i in range(1, len(videos)):
            if (videos[i]['time'] - videos[i-1]['time']) < timedelta(hours=4):
                current_group.append(videos[i])
            else:
                count += _process_video_group(target, current_group)
                current_group = [videos[i]]
        count += _process_video_group(target, current_group)
        return count
    except Exception as e:
        utils.log_error(f"영상 그룹화 프로세스 오류: {e}")
        return 0

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
