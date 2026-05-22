# [utils.py] - 공통 도구 및 정밀 보호 시스템 (v23 - Full Lock)
import os
import shutil
import datetime
import traceback
import time
import re
from pathlib import Path
import config

_current_log_file = None

def get_log_path():
    global _current_log_file
    if _current_log_file is None:
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = Path(config.BASE_LOG_DIR)
        try: base_dir.mkdir(parents=True, exist_ok=True)
        except: base_dir = Path.cwd()
        _current_log_file = base_dir / f"{config.LOG_FILE_PREFIX}_{now}.txt"
    return _current_log_file

def is_excluded(item_path):
    """파일 이름 및 상위 모든 경로에 대해 제외 목록 포함 여부를 완벽하게 검사합니다."""
    path_obj = Path(item_path).absolute()
    
    # 1. 제외 목록 정규화 (대소문자 무시, 공백 제거)
    clean_exclude = [str(ex).strip().lower() for ex in config.EXCLUDE_LIST]
    
    # 2. 파일 이름 체크
    if path_obj.name.lower() in clean_exclude:
        return True
        
    # 3. 경로의 모든 구성 요소 체크 (상위 폴더들)
    for part in path_obj.parts:
        if part.lower() in clean_exclude:
            return True
            
    # 4. 전체 경로 문자열 내 포함 여부 체크 (부분 일치)
    full_path_str = str(path_obj).lower()
    for ex in clean_exclude:
        if ex and ex in full_path_str:
            return True
            
    return False

def clean_filename_from_timestamps(filename):
    pattern = r'(_20\d{6}|_\d{6})'
    cleaned = re.sub(pattern, '', filename)
    return cleaned

def move_file(source, dest_dir):
    try:
        # [핵심] 이동 전 최종적으로 한 번 더 체크
        if is_excluded(source):
            return
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        pure_stem = clean_filename_from_timestamps(source.stem)
        dest = dest_dir / f"{pure_stem}{source.suffix}"
        
        if dest.exists():
            now = datetime.datetime.now().strftime("%H%M%S")
            dest = dest_dir / f"{pure_stem}_{now}{source.suffix}"
        
        max_retries = 3
        for i in range(max_retries):
            try:
                shutil.move(str(source), str(dest))
                print(f"✅ {source.name} -> {dest_dir.name}/")
                return
            except PermissionError:
                if i < max_retries - 1: time.sleep(1)
                else: raise
    except Exception as e:
        msg = f"이동 오류 ({source.name}): {str(e)}"
        print(f"❌ {msg}")
        log_error(msg)

def log_error(message, include_traceback=True):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(get_log_path(), "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [ERROR] {message}\n")
            if include_traceback:
                f.write(traceback.format_exc())
                f.write("-" * 50 + "\n")
    except: pass

def log_message(message, level="INFO"):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(get_log_path(), "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
    except: pass

def get_system_status():
    report = []
    report.append("=" * 60)
    report.append(f"🖥️ 시스템 정밀 진단 보고서 ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    report.append("-" * 60)
    report.append(f"[스캔 모드] {'Deep Scan' if config.RECURSIVE_SCAN else 'Quick Scan'}")
    report.append(f"[로그 경로] {get_log_path()}")
    report.append(f"[보호 목록] {config.EXCLUDE_LIST}")
    report.append("=" * 60)
    full_report = "\n".join(report)
    print(full_report)
    log_message("\n" + full_report, "DIAGNOSTIC")
    return full_report

def mark_empty_folders(target_path):
    try:
        for root, dirs, files in os.walk(target_path, topdown=False):
            for d in dirs:
                dir_path = Path(root) / d
                if is_excluded(dir_path): continue
                if not d.endswith("_빈폴더") and not any(dir_path.iterdir()):
                    if d[:2].isdigit() and "_" in d: continue
                    new_name = dir_path.parent / f"{d}_빈폴더"
                    try: dir_path.rename(new_name)
                    except: pass
    except Exception as e:
        log_error(f"빈 폴더 마킹 오류: {e}")

def validate_path(path_str):
    try:
        if not path_str: return None
        p = Path(path_str).absolute()
        return p if p.exists() else None
    except: return None
