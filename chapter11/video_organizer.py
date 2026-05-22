# [영상 그룹화 모듈: video_organizer.py]
import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

def run_video_grouping(target_path, time_threshold_hours=4):
    """메인 스크립트에서 호출할 영상 그룹화 함수입니다."""
    target = Path(target_path)
    video_extensions = [".mp4", ".mkv", ".avi", ".mov"]
    
    # 영상 파일 수집
    video_files = []
    for ext in video_extensions:
        for file in target.glob(f"*{ext}"):
            stat = file.stat()
            video_files.append({
                'path': file,
                'name': file.name,
                'time': datetime.fromtimestamp(stat.st_mtime)
            })
    
    if not video_files:
        return 0

    video_files.sort(key=lambda x: x['time'])
    
    # 그룹화 로직 (이전과 동일)
    groups = []
    current_group = [video_files[0]]
    for i in range(1, len(video_files)):
        if (video_files[i]['time'] - video_files[i-1]['time']) < timedelta(hours=time_threshold_hours):
            current_group.append(video_files[i])
        else:
            groups.append(current_group)
            current_group = [video_files[i]]
    groups.append(current_group)

    # 폴더 이동
    count = 0
    for i, group in enumerate(groups):
        folder_name = f"Video_Group_{group[0]['time'].strftime('%Y%m%d')}_{i+1}"
        group_path = target / "06_영상_그룹" / folder_name
        group_path.mkdir(parents=True, exist_ok=True)
        
        for file_info in group:
            shutil.move(str(file_info['path']), str(group_path / file_info['name']))
            count += 1
    
    return count
