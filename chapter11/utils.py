# [utils.py] - 공통 도구 함수 및 상세 오류 로깅 (v15)
import os
import shutil
import datetime
import traceback
from pathlib import Path

def log_error(message, include_traceback=True):
    """오류 내용을 error_log.txt 파일에 상세히 기록합니다."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
            if include_traceback:
                f.write(traceback.format_exc())
                f.write("-" * 50 + "\n")
    except:
        # 로그 기록조차 실패할 경우 콘솔에만 출력
        print(f"⚠️ 로그 기록 실패: {message}")

def move_file(source, dest_dir):
    """파일을 안전하게 이동 (이름 중복 및 권한 오류 방어)"""
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / source.name
        
        if dest.exists():
            timestamp = datetime.datetime.now().strftime("%H%M%S")
            dest = dest_dir / f"{source.stem}_{timestamp}{source.suffix}"
        
        shutil.move(str(source), str(dest))
        print(f"✅ {source.name} -> {dest_dir.name}/")
        
    except PermissionError:
        msg = f"❌ 권한 오류: {source.name} (파일이 사용 중일 수 있습니다.)"
        print(msg)
        log_error(msg)
    except Exception as e:
        msg = f"❌ 이동 오류 ({source.name}): {str(e)}"
        print(msg)
        log_error(msg)

def validate_path(path_str):
    """경로 유효성 검사"""
    try:
        if not path_str: return None
        p = Path(path_str)
        return p if p.exists() else None
    except Exception as e:
        log_error(f"경로 검증 오류: {str(e)}")
        return None
