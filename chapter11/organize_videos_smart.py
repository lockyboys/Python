import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta

def get_file_info(file_path):
    """파일의 수정 시간과 이름을 반환합니다."""
    stat = file_path.stat()
    return {
        'path': file_path,
        'name': file_path.name,
        'time': datetime.fromtimestamp(stat.st_mtime)
    }

def organize_videos_smart(target_path, time_threshold_hours=4):
    target = Path(target_path)
    if not target.exists():
        print(f"Error: {target_path} 경로를 찾을 수 없습니다.")
        return

    # 영상 확장자 정의
    video_extensions = [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"]
    
    # 영상 파일 정보 수집 및 시간순 정렬
    video_files = []
    for ext in video_extensions:
        for file in target.glob(f"*{ext}"):
            video_files.append(get_file_info(file))
    
    if not video_files:
        print("정리할 영상 파일이 없습니다.")
        return

    video_files.sort(key=lambda x: x['time'])

    print(f"🚀 총 {len(video_files)}개의 영상을 분석하여 그룹화를 시작합니다...")

    groups = []
    if video_files:
        current_group = [video_files[0]]
        
        for i in range(1, len(video_files)):
            prev_file = video_files[i-1]
            curr_file = video_files[i]
            
            # 1. 시간 간격 분석 (기본 4시간 이내면 같은 이벤트로 간주)
            time_diff = curr_file['time'] - prev_file['time']
            
            # 2. 이름 유사성 분석 (공통 단어 확인 - 간단한 구현)
            # 파일 이름의 앞 4글자가 같으면 연관된 것으로 간주
            name_match = curr_file['name'][:4] == prev_file['name'][:4]

            if time_diff < timedelta(hours=time_threshold_hours) or name_match:
                current_group.append(curr_file)
            else:
                groups.append(current_group)
                current_group = [curr_file]
        
        groups.append(current_group)

    # 그룹별 폴더 이동
    for i, group in enumerate(groups):
        # 그룹의 대표 날짜와 이름을 사용하여 폴더명 생성
        start_time = group[0]['time'].strftime("%Y%m%d")
        group_folder_name = f"Video_Group_{start_time}_{i+1}"
        
        group_path = target / "Organized_Videos" / group_folder_name
        group_path.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📂 그룹 생성: {group_folder_name} ({len(group)}개 영상)")
        
        for file_info in group:
            dest = group_path / file_info['name']
            shutil.move(str(file_info['path']), str(dest))
            print(f"  └─ {file_info['name']} 이동 완료")

    print("\n✨ 영상 그룹화 정리가 완료되었습니다!")

if __name__ == "__main__":
    print("=== 지능형 영상 그룹화 도구 (v4) ===")
    path_to_organize = input("영상들이 있는 폴더 경로를 입력하세요: ").strip()
    
    # 시간 임계값 설정 (기본 4시간)
    threshold = input("같은 그룹으로 묶을 시간 간격(시간 단위, 기본 4)을 입력하세요: ").strip()
    threshold = int(threshold) if threshold.isdigit() else 4
    
    organize_videos_smart(path_to_organize, threshold)
