# [utils.py] - 공통 도구 및 정밀 진단 시스템 (v17)
import os
import shutil
import traceback
import re

import config

from pathlib import Path
from datetime import datetime

_current_log_file = None    # 현재 실행 세션의 로그 파일 경로 (초기값 None)

# [복구] 파일명에서 날짜/시간 패턴 제거 함수 (v17 - Expert Fix)
def clean_filename_from_timestamps(filename):
    """파일명에서 반복되는 날짜/시간 패턴(_20260523_...)을 찾아 제거합니다."""
    # 8자리 날짜와 6자리 시간 패턴 (_20240101_123456 또는 _123456 등)을 매칭
    # 정규표현식: _20\d{6} (날짜) 또는 _\d{6} (시간)이 반복되는 것을 찾음
    pattern = r'(_20\d{6}|_\d{6})'
    cleaned = re.sub(pattern, '', filename)
    return cleaned

# [복구] log_error 함수 개선 (v17 - Expert Fix)
def log_error(message, include_traceback=True):
    """오류 내용을 로그 파일에 상세히 기록합니다. (이전 버전 호환성 유지)"""
    try:
        if not config.LoG_FILE_YN: return
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(get_log_path(), "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [ERROR] {message}\n")
            if include_traceback:
                f.write(traceback.format_exc())
                f.write("-" * 50 + "\n")
    except Exception as e:
        print(f"⚠️ 에러 로그 기록 실패: {e}")
        pass

# log_message 함수 추가 (일반 메시지 기록용)
def log_message(message, level="INFO"):
    """일반 메시지를 로그 파일에 기록합니다."""
    try:
        if not config.LoG_FILE_YN: return 
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(get_log_path(), "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")
    except Exception as e:
        print(f"⚠️ 로그 메시지 기록 실패: {e}")
        pass

# get_log_path 함수 추가 (로그 파일 경로 관리)
def get_log_path():
    global _current_log_file
    if _current_log_file is None:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = Path(config.BASE_LOG_DIR)
        try: base_dir.mkdir(parents=True, exist_ok=True)
        except: base_dir = Path.cwd()
        _current_log_file = base_dir / f"{config.LOG_FILE_PREFIX}_{now}.txt"
    return _current_log_file

# 문서 분석 라이브러리 로드 시도 및 상태 플래그 설정 (v17 - Expert Fix)
def is_excluded(item_path):
    """파일 이름 및 상위 모든 경로에 대해 제외 목록 포함 여부를 완벽하게 검사합니다."""
    path_obj = Path(item_path).absolute()
    # 1. 제외 목록 정규화 (대소문자 무시, 공백 제거)
    clean_exclude = [str(ex).strip().lower() for ex in config.EXCLUDE_LIST]
    # 2. 파일 이름 체크
    if path_obj.name.lower() in clean_exclude: return True
    # 3. 경로의 모든 구성 요소 체크 (상위 폴더들)
    for part in path_obj.parts:
        if part.lower() in clean_exclude: return True
    # 4. 전체 경로 문자열 내 포함 여부 체크 (부분 일치)
    full_path_str = str(path_obj).lower()
    for ex in clean_exclude:
        if ex and ex in full_path_str: return True
    return False

def get_system_status():
    """모든 라이브러리 및 하드웨어 상태를 정밀 진단하여 보고합니다."""
    report = []
    report.append("=" * 60)
    report.append(f"🖥️ 시스템 정밀 진단 보고서 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    report.append("-" * 60)
    
    # 1. 스캔 및 제어 설정
    report.append(f"[스캔 모드] {'Deep Scan (하위 포함)' if config.RECURSIVE_SCAN else 'Quick Scan (현재 폴더만)'}")
    report.append(f"[해체 모드] {'UNPACK ALL (전체 해체)' if config.UNPACK_ALL else '구조 유지'}")
    report.append(f"[출력 모드] {'실시간 중계 활성' if config.SHOW_PROGRESS else '로그만 기록'}")
    report.append(f"[로그 경로] {config.LOG_FILE_PATH}")
    report.append(f"[보호 목록] {config.EXCLUDE_LIST}")
    
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
    """파일 이동 (중복 시 기존 시간 제거 후 최신 시간 1개만 유지)"""
    try:
        # [핵심] 이동 전 최종적으로 한 번 더 체크
        if is_excluded(source): return
        
        if source.name in config.EXCLUDE_LIST: return # 파일명 자체가 제외 리스트에 있는 경우 (안전망)

        if dest_dir.name in config.EXCLUDE_LIST: return # 대상 폴더명이 제외 리스트에 있는 경우 (안전망)
        # 1. 원본 파일명에서 지저분한 이전 시간 패턴 제거
        dest_dir.mkdir(parents=True, exist_ok=True) # 대상 폴더가 없으면 생성 (중간 폴더도 함께)
        clean_filename = clean_filename_from_timestamps(source.name) # 파일명에서 날짜/시간 패턴 제거
        dest = dest_dir / f"{clean_filename}{source.suffix}" # 최종 대상 경로 (날짜/시간 패턴 제거된 이름)

        # 2. 목적지에 이미 파일이 있다면 최신 시간 하나만 붙임
        if dest.exists():
            now = datetime.datetime.now().strftime("%H%M%S")
            dest = dest_dir / f"{clean_filename}_{now}{source.suffix}"        
        
        # 3. 파일 이동 (재시도 로직 포함)
        max_retries = 3
        for i in range(max_retries):
            try:
                shutil.move(str(source), str(dest))
                # - 1. 화면(콘솔) 출력 여부 결정
                status_msg = f"✅ {source.name} -> {dest_dir.name}/{dest.name} "
                if config.SHOW_PROGRESS:
                    print(status_msg)
                
                # - 2. 로그 파일에 이동 기록 저장 (항상 기록)
                log_message(f"MOVE_SUCCESS: {source.absolute()} -> {dest.absolute()}")
                return
            except PermissionError:
                if i < max_retries - 1: datetime.time.sleep(1)
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
                if is_excluded(dir_path): continue
                if not d.endswith("_빈폴더") and not any(dir_path.iterdir()):
                    if d[:2].isdigit() and "_" in d: continue
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
