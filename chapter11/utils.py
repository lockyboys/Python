# [utils.py] - 공통 도구 함수 및 상세 진단 시스템 (v16)
import os
import shutil
import datetime
import traceback
import sys
from pathlib import Path
import config

def log_message(message, level="INFO", include_traceback=False):
    """메시지를 로그 파일에 기록합니다."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = Path(config.LOG_FILE_PATH)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
            if include_traceback:
                f.write(traceback.format_exc())
                f.write("-" * 50 + "\n")
    except Exception as e:
        print(f"⚠️ 로그 기록 실패: {e}")

def get_system_status():
    """시스템 및 라이브러리 작동 상태를 상세히 체크하여 보고합니다."""
    report = []
    report.append("=" * 60)
    report.append(f"🖥️ 시스템 진단 보고서 ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    report.append("-" * 60)
    
    # 1. 스캔 모드
    report.append(f"[스캔 모드] {'Deep Scan (하위 포함)' if config.RECURSIVE_SCAN else 'Quick Scan (현재 폴더만)'}")
    report.append(f"[해체 모드] {'UNPACK ALL 활성화' if config.UNPACK_ALL else '구조 유지'}")
    
    # 2. GPU 및 TensorFlow 상태
    try:
        import tensorflow as tf
        report.append(f"[TensorFlow] 버전 {tf.__version__} - 설치됨")
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            report.append(f"[GPU 상태] ✅ {len(gpus)}개 감지됨")
            for i, gpu in enumerate(gpus):
                report.append(f"   - GPU [{i}]: {gpu.name}")
            # CUDA/cuDNN 상세 (TF 내부 정보를 통해 유추)
            report.append(f"[CUDA/cuDNN] 가속 엔진 활성화됨")
        else:
            report.append("[GPU 상태] ℹ️ 감지되지 않음 (CPU 모드)")
    except Exception as e:
        report.append(f"[TensorFlow/GPU] ❌ 로드 실패: {e}")

    # 3. OpenCV 상태
    try:
        import cv2
        report.append(f"[OpenCV] 버전 {cv2.__version__} - ✅ 정상")
    except Exception as e:
        report.append(f"[OpenCV] ❌ 로드 실패: {e}")

    # 4. Tesseract OCR 상태
    try:
        import pytesseract
        # 실제 엔진 설치 여부 확인 시도
        ver = pytesseract.get_tesseract_version()
        report.append(f"[Tesseract OCR] 버전 {ver} - ✅ 정상")
    except Exception as e:
        report.append(f"[Tesseract OCR] ❌ 엔진 미설치 또는 로드 실패: {e}")

    # 5. 문서 분석 라이브러리 상태
    libs = {
        "PyMuPDF(fitz)": "fitz",
        "python-docx": "docx",
        "openpyxl": "openpyxl",
        "python-pptx": "pptx",
        "olefile": "olefile"
    }
    for name, mod in libs.items():
        try:
            __import__(mod)
            report.append(f"[{name}] ✅ 준비됨")
        except:
            report.append(f"[{name}] ⚠️ 미설치")

    report.append("=" * 60)
    full_report = "\n".join(report)
    print(full_report)
    log_message("\n" + full_report, "DIAGNOSTIC")
    return full_report

def move_file(source, dest_dir):
    """파일을 안전하게 이동 (중복 시 날짜_시간 추가)"""
    try:
        # 제외 리스트 확인
        if source.name in config.EXCLUDE_LIST:
            return
            
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
        log_message(msg, "ERROR", True)

def mark_empty_folders(target_path):
    """내용물이 없는 폴더를 찾아 '_빈폴더' 마킹을 추가합니다."""
    try:
        # 하위 폴더부터 거꾸로 탐색 (안쪽 빈 폴더부터 처리)
        for root, dirs, files in os.walk(target_path, topdown=False):
            for d in dirs:
                dir_path = Path(root) / d
                # 이미 '_빈폴더'가 붙어있지 않고, 내용물이 없는 경우
                if not d.endswith("_빈폴더") and not any(dir_path.iterdir()):
                    new_name = dir_path.parent / f"{d}_빈폴더"
                    dir_path.rename(new_name)
                    print(f"📁 빈 폴더 마킹: {d} -> {new_name.name}")
    except Exception as e:
        log_message(f"빈 폴더 마킹 중 오류: {e}", "ERROR")

def validate_path(path_str):
    try:
        if not path_str: return None
        p = Path(path_str)
        return p if p.exists() else None
    except Exception as e:
        log_message(f"경로 검증 오류: {str(e)}", "ERROR")
        return None
