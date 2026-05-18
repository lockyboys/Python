# [최종 메인 스크립트: organize_master_v8.py]

import config           # 1. 설정 파일 연결
import utils            # 2. 유틸리티 파일 연결
import video_organizer  # 3. ★외부 영상 그룹화 소스 연결★ (이 문구가 핵심입니다!)

def start_master_process(target_path):
    target = utils.check_path_valid(target_path)
    if not target: return

    print(f"🚀 통합 정리를 시작합니다...\n")

    # [기능 1] 외부 소스(video_organizer) 호출하여 영상 그룹화 실행
    # 이 부분이 바로 다른 소스 파일로 '흐름'이 넘어가는 지점입니다.
    print("🎬 영상 지능형 그룹화를 시작합니다 (외부 모듈 호출)...")
    video_count = video_organizer.run_video_grouping(target_path)
    print(f"✅ {video_count}개의 영상이 그룹화되었습니다.\n")

    # [기능 2] 나머지 파일들에 대한 키워드 및 확장자 정리 (기존 로직)
    print("📂 나머지 파일들에 대한 정리를 시작합니다...")
    other_count = 0
    for item in target.iterdir():
        if item.is_dir() or item.name.startswith("organize_") or item.name in ["config.py", "utils.py", "video_organizer.py"]:
            continue
        
        filename = item.name
        extension = item.suffix.lower()
        moved = False

        # 키워드 분석 (config 연결)
        for folder, keywords in config.KEYWORD_RULES.items():
            if any(kw in filename for kw in keywords):
                utils.move_file_safely(item, target / folder)
                moved = True
                break
        
        if not moved:
            # 일반 이미지 처리 (config 연결)
            if extension in config.IMAGE_EXTENSIONS:
                utils.move_file_safely(item, target / "09_일반_사진")
                moved = True
        
        if moved: other_count += 1

    print(f"\n✨ 모든 작업 완료! (영상: {video_count}, 기타: {other_count})")

if __name__ == "__main__":
    path = input("정리할 폴더 경로를 입력하세요: ").strip()
    start_master_process(path)
