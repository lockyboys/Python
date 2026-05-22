# [utils.py] - 공통 도구 및 스마트 네이밍 시스템 (v22)
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
    path_obj = Path(item_path)
    if path_obj.name in config.EXCLUDE_LIST: return True
    for parent in path_obj.parents:
        if parent.name in config.EXCLUDE_LIST: return True
    path_str = str(item_path)
    for ex in config.EXCLUDE_LIST:
        if ex in path_str: return True
    return False

def clean_filename_from_timestamps(filename):
    """파일명에서 반복되는 날짜/시간 패턴(_20260523_...)을 찾아 제거합니다."""
    # 8자리 날짜와 6자리 시간 패턴 (_20240101_123456 또는 _123456 등)을 매칭
    # 정규표현식: _20\d{6} (날짜) 또는 _\d{6} (시간)이 반복되는 것을 찾음
    pattern = r'(_20\d{6}|_\d{6})'
    cleaned = re.sub(pattern, '', filename)
    return cleaned

def move_file(source, dest_dir):
    """파일 이동 (중복 시 기존 시간 제거 후 최신 시간 1개만 유지)"""
    try:
        if is_excluded(source): return
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. 원본 파일명에서 지저분한 이전 시간 패턴 제거
        pure_stem = clean_filename_from_timestamps(source.stem)
        dest = dest_dir / f"{pure_stem}{source.suffix}"
        
        # 2. 목적지에 이미 파일이 있다면 최신 시간 하나만 붙임
        if dest.exists():
            now = datetime.datetime.now().strftime("%H%M%S")
            dest = dest_dir / f"{pure_stem}_{now}{source.suffix}"
        
        # 3. 파일 이동 (재시도 로직 포함)
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
        p = Path(path_str)
        return p if p.exists() else None
    except: return None
