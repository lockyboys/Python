# [video_analyzer.py] - 영상 지능형 그룹화 전문 모듈
from pathlib import Path
from datetime import datetime, timedelta
import config
import utils

def group_videos(target_path):
    """영상들을 시간대별로 그룹화하여 정리..."""
    target = Path(target_path)
    videos = []
    for ext in config.VIDEO_EXTENSIONS:
        for f in target.glob(f"*{ext}"):
            videos.append({'path': f, 'time': datetime.fromtimestamp(f.stat().st_mtime)})
    
    if not videos: return 0
    videos.sort(key=lambda x: x['time'])

    count = 0
    if videos:
        current_group = [videos[0]]
        for i in range(1, len(videos)):
            if (videos[i]['time'] - videos[i-1]['time']) < timedelta(hours=4):
                current_group.append(videos[i])
            else:
                count += _move_group(target, current_group)
                current_group = [videos[i]]
        count += _move_group(target, current_group)
    return count

def _move_group(target, group):
    folder = target / "06_영상_그룹" / f"Group_{group[0]['time'].strftime('%Y%m%d_%H%M')}"
    for v in group:
        utils.move_file(v['path'], folder)
    return len(group)
