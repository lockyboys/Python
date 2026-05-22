# [video_analyzer.py] - 영상 지능형 그룹화 및 AI 내용 분석 모듈 (v13 - Multi-Frame Analysis)
import os
import cv2
from pathlib import Path
from datetime import datetime, timedelta
import config
import utils
import image_analyzer
from collections import Counter

# --- 분석 설정 변수 (사용자가 직접 조절 가능) ---
MINUTES_PER_FRAME = 10  # 몇 분당 1장의 사진을 추출할지 설정 (예: 10분당 1장)
MAX_FRAMES_PER_VIDEO = 20  # 한 영상에서 추출할 최대 사진 장수 (안전장치)
# ------------------------------------------

def group_videos(target_path):
    """영상들을 시간대별로 그룹화하고 AI로 내용을 분석하여 정리"""
    target = Path(target_path)
    videos = []
    
    for f in target.rglob('*'):
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

def _process_video_group(target, group):
    """그룹화된 영상의 내용을 AI로 분석하고 이동"""
    # 그룹 내 모든 영상에 대해 다중 프레임 분석 수행
    all_categories = []
    for v in group:
        categories = _analyze_video_multi_frames(v['path'])
        all_categories.extend(categories)
    
    # 가장 많이 등장한 카테고리를 대표 카테고리로 선정 (다수결)
    if all_categories:
        most_common = Counter(all_categories).most_common(1)[0][0]
        analysis_result = most_common
    else:
        analysis_result = "일반영상"
    
    # 카테고리 이름 정제 (예: '07_동물_및_생물' -> '동물_및_생물')
    if "_" in analysis_result and analysis_result[:2].isdigit():
        analysis_result = analysis_result.split("_", 1)[1]
    
    folder_prefix = f"Group_{group[0]['time'].strftime('%Y%m%d_%H%M')}"
    folder_name = f"{folder_prefix}_{analysis_result}"
    
    dest_dir = target / "06_영상_그룹" / folder_name
    
    for v in group:
        utils.move_file(v['path'], dest_dir)
    return len(group)

def _analyze_video_multi_frames(video_path):
    """설정된 시간 간격에 따라 여러 프레임을 추출하여 AI로 분석"""
    categories = []
    try:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return []
            
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = total_frames / fps if fps > 0 else 0
        
        # 분석할 프레임 위치 계산 (10분당 1장)
        interval_sec = MINUTES_PER_FRAME * 60
        num_frames_to_extract = min(int(duration_sec / interval_sec) + 1, MAX_FRAMES_PER_VIDEO)
        
        # 최소 1장은 추출 (영상이 10분보다 짧더라도)
        if num_frames_to_extract == 0:
            num_frames_to_extract = 1
            
        print(f"🎬 영상 분석 중: {video_path.name} ({int(duration_sec)}초, {num_frames_to_extract}개 프레임 추출)")
        
        for i in range(num_frames_to_extract):
            # 프레임 위치 선정 (영상을 균등하게 나눔)
            if num_frames_to_extract == 1:
                target_frame = total_frames // 2
            else:
                target_frame = int((total_frames / num_frames_to_extract) * i + (total_frames / (num_frames_to_extract * 2)))
            
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            ret, frame = cap.read()
            
            if ret:
                temp_img_path = Path(f"temp_frame_{i}.jpg")
                cv2.imwrite(str(temp_img_path), frame)
                
                # AI 분석 호출
                category = image_analyzer.analyze_image_final(temp_img_path)
                categories.append(category)
                
                if temp_img_path.exists():
                    temp_img_path.unlink()
        
        cap.release()
        return categories
        
    except Exception as e:
        # utils.log_error가 없는 경우 대비
        with open("error_log.txt", "a", encoding="utf-8") as f:
            import datetime
            f.write(f"[{datetime.datetime.now()}] 영상 분석 오류 ({video_path.name}): {e}\n")
        return []
