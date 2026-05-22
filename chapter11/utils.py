# [utils.py] - 공통 도구 함수 및 오류 로깅 (v10)
import os
import shutil
import datetime
from pathlib import Path

def log_error(message):
    """오류 내용을 error_log.txt 파일에 기록합니다."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass

def move_file(source, dest_dir):
    """파일을 안전하게 이동 (이름 중복 및 권한 오류 방어)"""
    try:
        # 상위 폴더까지 한꺼번에 생성
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        dest = dest_dir / source.name
        
        # 동일한 이름의 파일이 이미 있는 경우 이름 뒤에 시간값 추가
        if dest.exists():
            timestamp = int(os.path.getmtime(source))
            dest = dest_dir / f"{source.stem}_{timestamp}{source.suffix}"
        
        # 파일 이동 실행
        shutil.move(str(source), str(dest))
        print(f"✅ {source.name} -> {dest_dir.name}/")
        
    except PermissionError:
        msg = f"❌ 권한 오류: {source.name} (파일이 사용 중일 수 있습니다.)"
        print(msg)
        log_error(msg)
    except Exception as e:
        msg = f"❌ 알 수 없는 오류 ({source.name}): {str(e)}"
        print(msg)
        log_error(msg)

def validate_path(path_str):
    """경로 유효성 검사"""
    try:
        if not path_str: return None
        p = Path(path_str)
        return p if p.exists() else None
    except:
        return None
