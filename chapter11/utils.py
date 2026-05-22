# [utils.py] - 공통 도구 및 정밀 폴더 관리 시스템 (v19)
import os
import shutil
import datetime
import traceback
import time
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
    report.append(f"[스캔 모드] {'Deep Scan (하위 포함)' if config.RECURSIVE_SCAN else 'Quick Scan (현재 폴더만)'}")
    report.append(f"[해체 모드] {'UNPACK ALL' if config.UNPACK_ALL else '구조 유지'}")
    report.append(f"[로그 경로] {get_log_path()}")
    
    try:
        import tensorflow as tf
        report.append(f"[TensorFlow] 버전 {tf.__version__} - ✅ 로드 성공")
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            report.append(f"[GPU/CUDA] ✅ NVIDIA GPU {len(gpus)}개 감지됨")
            report.append("[cuDNN] ✅ 가속 엔진 준비 완료")
        else: report.append("[GPU/CUDA] ℹ️ GPU 미감지")
    except: report.append("[TensorFlow/GPU] ❌ 진단 실패")

    try:
        import cv2
        report.append(f"[OpenCV] 버전 {cv2.__version__} - ✅ 정상")
    except: report.append("[OpenCV] ❌ 로드 실패")

    try:
        import pytesseract
        report.append(f"[Tesseract OCR] ✅ 정상")
    except: report.append("[Tesseract OCR] ❌ 로드 실패")

    report.append("=" * 60)
    full_report = "\n".join(report)
    print(full_report)
    log_message("\n" + full_report, "DIAGNOSTIC")
    return full_report

def move_file(source, dest_dir):
    """파일 이동 (중복 시 날짜_시간, 잠김 시 재시도)"""
    try:
        if source.name in config.EXCLUDE_LIST: return
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / source.name
        
        if dest.exists():
            now = datetime.datetime.now().strftime("%H%M%S")
            dest = dest_dir / f"{source.stem}_{now}{source.suffix}"
        
        # 파일 잠김(PermissionError) 대응을 위한 재시도 로직
        max_retries = 3
        for i in range(max_retries):
            try:
                shutil.move(str(source), str(dest))
                print(f"✅ {source.name} -> {dest_dir.name}/")
                return
            except PermissionError:
                if i < max_retries - 1:
                    time.sleep(1) # 1초 대기 후 재시도
                else: raise
    except Exception as e:
        msg = f"이동 오류 ({source.name}): {str(e)}"
        print(f"❌ {msg}")
        log_error(msg)

def mark_empty_folders(target_path):
    """빈 폴더를 찾아 '_빈폴더' 마킹 추가"""
    try:
        for root, dirs, files in os.walk(target_path, topdown=False):
            for d in dirs:
                dir_path = Path(root) / d
                if not d.endswith("_빈폴더") and not any(dir_path.iterdir()):
                    # 번호가 붙은 시스템 생성 폴더는 마킹 제외
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
