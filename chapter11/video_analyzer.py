# [video_analyzer.py] - 영상 지능형 그룹화 및 AI 내용 분석 모듈 (v11)
import os
import cv2
from pathlib import Path
from datetime import datetime, timedelta
import config
import utils
import image_analyzer

def group_videos(target_path):
    """영상들을 시간대별로 그룹화하고 AI로 내용을 분석하여 정리"""
    target = Path(target_path)
    videos = []
    
    # rglob을 사용하여 모든 하위 폴더의 영상 수집
    for f in target.rglob('*'):
        if f.is_file() and f.suffix.lower() in config.VIDEO_EXTENSIONS:
            # 이미 분류된 폴더에 있는 경우 제외
            if any(p.name.startswith(('0', '영상_그룹')) for p in f.parents if p != target):
                continue
            videos.append({'path': f, 'time': datetime.fromtimestamp(f.stat().st_mtime)})
    
    if not videos: return 0
    
    # 시간순 정렬
    videos.sort(key=lambda x: x['time'])

    count = 0
    current_group = [videos[0]]
    for i in range(1, len(videos)):
        # 4시간 이내의 영상은 같은 그룹으로 묶음
        if (videos[i]['time'] - videos[i-1]['time']) < timedelta(hours=4):
            current_group.append(videos[i])
        else:
            count += _process_video_group(target, current_group)
            current_group = [videos[i]]
            
    # 마지막 그룹 처리
    count += _process_video_group(target, current_group)
    return count

def _process_video_group(target, group):
    """그룹화된 영상의 내용을 AI로 분석하고 이동"""
    # 그룹 내 첫 번째 영상의 대표 프레임을 추출하여 내용 분석
    representative_video = group[0]['path']
    analysis_result = _analyze_video_content(representative_video)
    
    # 분석 결과에 따른 폴더 이름 결정
    folder_prefix = f"Group_{group[0]['time'].strftime('%Y%m%d_%H%M')}"
    folder_name = f"{folder_prefix}_{analysis_result}"
    
    dest_dir = target / "06_영상_그룹" / folder_name
    
    for v in group:
        utils.move_file(v['path'], dest_dir)
    return len(group)

def _analyze_video_content(video_path):
    """영상의 중간 프레임을 추출하여 AI로 분석"""
    try:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            return "일반영상"
            
        # 전체 프레임 수 확인
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # 영상의 중간 지점(50%) 프레임 번호 계산
        middle_frame_idx = total_frames // 2
        
        # 중간 프레임으로 이동
        cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_idx)
        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return "일반영상"
            
        # 임시 이미지 파일로 저장하여 image_analyzer에게 전달
        temp_img_path = Path("temp_video_frame.jpg")
        cv2.imwrite(str(temp_img_path), frame)
        
        # image_analyzer의 AI 분석 기능 활용
        category = image_analyzer.analyze_image_final(temp_img_path)
        
        # 임시 파일 삭제
        if temp_img_path.exists():
            temp_img_path.unlink()
            
        # 카테고리 이름에서 번호 제거 (예: '07_동물_및_생물' -> '동물_및_생물')
        if "_" in category and category[:2].isdigit():
            return category.split("_", 1)[1]
        return category
        
    except Exception as e:
        utils.log_error(f"영상 분석 오류 ({video_path.name}): {e}")
        return "일반영상"
