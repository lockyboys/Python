# [utils.py] - 공통 도구 및 정밀 로깅 시스템 (v25)
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
    path_obj = Path(item_path).absolute()
    clean_exclude = [str(ex).strip().lower() for ex in config.EXCLUDE_LIST]
    if path_obj.name.lower() in clean_exclude: return True
    for part in path_obj.parts:
        if part.lower() in clean_exclude: return True
    full_path_str = str(path_obj).lower()
    for ex in clean_exclude:
        if ex and ex in full_path_str: return True
    return False

def clean_filename_from_timestamps(filename):
    pattern = r'(_20\d{6}|_\d{6})'
    cleaned = re.sub(pattern, '', filename)
    return cleaned

def move_file(source, dest_dir):
    """파일 이동 및 상세 로그 기록 (화면 출력은 선택적)"""
    try:
        if is_excluded(source): return
        
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
                # 1. 화면(콘솔) 출력 여부 결정
                status_msg = f"✅ {source.name} -> {dest_dir.name}/"
                if config.SHOW_PROGRESS:
                    print(status_msg)
                
                # 2. 로그 파일에 이동 기록 저장 (항상 기록)
                log_message(f"MOVE_SUCCESS: {source.absolute()} -> {dest.absolute()}")
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
    report.append(f"[출력 모드] {'실시간 중계 활성' if config.SHOW_PROGRESS else '로그만 기록'}")
    report.append(f"[로그 경로] {get_log_path()}")
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
