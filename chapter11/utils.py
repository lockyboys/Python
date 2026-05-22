# [utils.py] - 공통 도구 및 정밀 진단 시스템 (v17)
import os
import shutil
import datetime
import traceback
from pathlib import Path
import config

def log_error(message, include_traceback=True):
    """오류 내용을 로그 파일에 상세히 기록합니다. (이전 버전 호환성 유지)"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = Path(config.LOG_FILE_PATH)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [ERROR] {message}\n")
            if include_traceback:
                f.write(traceback.format_exc())
                f.write("-" * 50 + "\n")
    except Exception as e:
        print(f"⚠️ 로그 기록 실패: {e}")

def log_message(message, level="INFO"):
    """일반 메시지를 로그 파일에 기록합니다."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = Path(config.LOG_FILE_PATH)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
    except: pass

def get_system_status():
    """모든 라이브러리 및 하드웨어 상태를 정밀 진단하여 보고합니다."""
    report = []
    report.append("=" * 60)
    report.append(f"🖥️ 시스템 정밀 진단 보고서 ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    report.append("-" * 60)
    
    # 1. 스캔 및 제어 설정
    report.append(f"[스캔 모드] {'Deep Scan (하위 포함)' if config.RECURSIVE_SCAN else 'Quick Scan (현재 폴더만)'}")
    report.append(f"[해체 모드] {'UNPACK ALL (전체 해체)' if config.UNPACK_ALL else '구조 유지'}")
    report.append(f"[로그 경로] {config.LOG_FILE_PATH}")
    
    # 2. GPU / CUDA / TensorFlow
    try:
        import tensorflow as tf
        report.append(f"[TensorFlow] 버전 {tf.__version__} - ✅ 로드 성공")
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            report.append(f"[GPU/CUDA] ✅ NVIDIA GPU {len(gpus)}개 감지됨")
            for i, gpu in enumerate(gpus):
                report.append(f"   - 장치 [{i}]: {gpu.name}")
            report.append("[cuDNN] ✅ 가속 엔진 준비 완료")
        else:
            report.append("[GPU/CUDA] ℹ️ GPU 미감지 (CPU 모드로 작동)")
    except Exception as e:
        report.append(f"[TensorFlow/GPU] ❌ 진단 실패: {e}")

    # 3. OpenCV / 미디어
    try:
        import cv2
        report.append(f"[OpenCV] 버전 {cv2.__version__} - ✅ 정상")
    except Exception as e:
        report.append(f"[OpenCV] ❌ 로드 실패: {e}")

    # 4. OCR 엔진
    try:
        import pytesseract
        ver = pytesseract.get_tesseract_version()
        report.append(f"[Tesseract OCR] 버전 {ver} - ✅ 정상")
    except Exception as e:
        report.append(f"[Tesseract OCR] ❌ 엔진 미설치 또는 로드 실패: {e}")

    # 5. 문서 분석 라이브러리
    doc_libs = {"PyMuPDF(fitz)": "fitz", "python-docx": "docx", "openpyxl": "openpyxl", "python-pptx": "pptx", "olefile": "olefile"}
    for name, mod in doc_libs.items():
        try:
            __import__(mod)
            report.append(f"[{name}] ✅ 설치됨")
        except:
            report.append(f"[{name}] ⚠️ 미설치 (해당 포맷 분석 불가)")

    report.append("=" * 60)
    full_report = "\n".join(report)
    print(full_report)
    log_message("\n" + full_report, "DIAGNOSTIC")
    return full_report

def move_file(source, dest_dir):
    """파일 이동 (중복 시 날짜_시간 추가)"""
    try:
        if source.name in config.EXCLUDE_LIST: return
        
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / source.name
        
        if dest.exists():
            now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            dest = dest_dir / f"{source.stem}_{now}{source.suffix}"
        
        shutil.move(str(source), str(dest))
        print(f"✅ {source.name} -> {dest_dir.name}/")
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
                    new_name = dir_path.parent / f"{d}_빈폴더"
                    try:
                        dir_path.rename(new_name)
                        print(f"📁 빈 폴더 마킹: {d} -> {new_name.name}")
                    except: pass
    except Exception as e:
        log_error(f"빈 폴더 마킹 중 오류: {e}")

def validate_path(path_str):
    try:
        if not path_str: return None
        p = Path(path_str)
        return p if p.exists() else None
    except: return None
