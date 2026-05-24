# [utils.py] - 공통 도구 및 정밀 진단 시스템 (v17)
import os
import config
import shutil
import traceback
import re
import time

from pathlib import Path
from datetime import datetime

# --------------------------------
# [개선] 로그 파일 경로 관리 및 오류 기록 개선 (v17 - Expert Fix)
# [개선] 로그 파일 경로를 전역 변수로 관리하여 일관된 기록 보장
# [개선] log_error 함수 개선하여 상세 오류 기록 및 예외 처리 강화
# [개선] get_log_path 함수 추가하여 로그 파일 경로 생성 및 관리
# --------------------------------
_current_log_file = None    # 현재 실행 세션의 로그 파일 경로 (초기값 None)
# --------------------------------
# [복구] 파일명에서 날짜/시간 패턴1 제거 함수 (v17 - Expert Fix11)
# [개선] 파일명에서 반복되는 날짜/시간 패턴(_20260523_...)을 찾아 제거하는 함수 추가
# [개선] 정규표현식을 사용하여 다양한 날짜/시간 패턴을 제거하도록 개선
# --------------------------------  
def cleaning_filename(filename):
    """ 파일명에서 반복되는 날짜/시간 패턴(_20260523_...)을 찾아 제거합니다.
        photo.jpg.jpg.jpg -> photo.jpg
        document.pdf.pdf -> document.pdf
    """
    # 파일명과 확장자 분리
    

    # 8자리 날짜와 6자리 시간 패턴 (_20240101_123456 또는 _123456 등)을 매칭
    # 정규표현식: _20\d{6} (날짜) 또는 _\d{6} (시간)이 반복되는 것을 찾음
    pattern = r'(_20\d{6}|_\d{6})'
    cleaned = re.sub(pattern, '', filename)

    # 반복 확장자 제거
    pattern = r'(\.[a-zA-Z0-9]+)(\1)+$'
    cleaned = re.sub(pattern, '', filename)

    return cleaned
# --------------------------------
# [복구] log_error 함수 개선 (v17 - Expert Fix)
# [개선] log_error 함수 개선하여 상세 오류 기록 및 예외 처리 강화
# [개선] get_log_path 함수 추가하여 로그 파일 경로 생성 및 관리
# --------------------------------
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
# --------------------------------
# log_message 함수 추가 (일반 메시지 기록용)
# [개선] log_message 함수 추가하여 일반 메시지를 로그 파일에 기록할 수 있도록 개선
# [개선] 로그 메시지 기록 시 타임스탬프와 레벨을 함께 기록하도록 개선
# [개선] 로그 메시지 기록 실패 시 예외 처리 강화
# --------------------------------
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
# --------------------------------
# get_log_path 함수 추가 (로그 파일 경로 관리)
# [개선] get_log_path 함수 추가하여 로그 파일 경로 생성 및 관리
# [개선] 로그 파일은 실행 시점에 한 번 생성되며, 이후 모든 로그 기록은 이 파일에 일관되게 기록됩니다.
# [개선] 로그 파일 생성 시점에 타임스탬프를 포함하여 고유한 파일명을 생성하도록 개선
# [개선] 로그 파일 생성 실패 시 예외 처리 강화
# --------------------------------
def get_log_path():
    global _current_log_file
    if _current_log_file is None:
        now = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_dir = Path(config.BASE_LOG_DIR)
        try: base_dir.mkdir(parents=True, exist_ok=True)
        except: base_dir = Path.cwd()
        _current_log_file = base_dir / f"{config.LOG_FILE_PREFIX}_{now}.txt"
    return _current_log_file
# --------------------------------
# 문서 분석 라이브러리 로드 시도 및 상태 플래그 설정 (v17 - Expert Fix)
# [개선] 라이브러리 로드 실패 시에도 시스템이 계속 작동하도록 예외 처리 강화
# [개선] 각 라이브러리 로드 시 상세 오류 로그 기록
# [개선] 문서 분석에 필요한 라이브러리 로드 시도 및 상태 플래그 설정 
# --------------------------------
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
# --------------------------------
# 시스템 상태 정밀 진단 함수 (v17 - Expert Fix)
# [개선] 시스템 상태 정밀 진단 함수 추가하여 라이브러리 및 하드웨어 상태를 상세히 보고하도록 개선
# [개선] 진단 보고서에는 스캔 및 제어 설정, GPU/CUDA/TensorFlow 상태, OpenCV 상태, OCR 엔진 상태, 문서 분석 라이브러리 상태 등이 포함됩니다.
# [개선] 진단 과정에서 발생하는 오류는 상세히 로그에 기록하되, 시스템이 계속 작동하도록 예외 처리 강화
# --------------------------------
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
        report.append(f"[TensorFlow] 버전 {tf.__version__} - \t\t\t\t✅ 로드 성공")
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            report.append(f"[GPU/CUDA] \t\t\t\t\t\t\t\t✅ NVIDIA GPU {len(gpus)}개 감지됨")
            for i, gpu in enumerate(gpus):
                report.append(f"   - 장치 [{i}]: {gpu.name}")
            report.append("[cuDNN] \t\t\t\t\t\t\t\t✅ 가속 엔진 준비 완료")
        else:
            report.append("[GPU/CUDA] \t\t\t\t\tℹ️ GPU 미감지 (CPU 모드로 작동)")
    except Exception as e:
        report.append(f"[TensorFlow/GPU] \t\t\t\t\t❌ 진단 실패: {e}")

    # 3. OpenCV / 미디어
    try:
        import cv2
        report.append(f"[OpenCV] 버전 {cv2.__version__} - \t\t\t\t\t✅ 정상")
    except Exception as e:
        report.append(f"[OpenCV] \t\t\t\t\t\t❌ 로드 실패: {e}")

    # 4. OCR 엔진
    try:
        import pytesseract
        ver = pytesseract.get_tesseract_version()
        report.append(f"[Tesseract OCR] 버전 {ver} - \t✅ 정상")
    except Exception as e:
        report.append(f"[Tesseract OCR] \t\t\t\t\t\t❌ 엔진 미설치 또는 로드 실패: {e}")

    # 5. 문서 분석 라이브러리
    doc_libs = {"PyMuPDF(fitz)": "fitz", "python-docx": "docx", "openpyxl": "openpyxl", "python-pptx": "pptx", "olefile": "olefile"}
    for name, mod in doc_libs.items():
        try:
            __import__(mod)
            report.append(f"[{name}] \t\t\t\t\t\t✅ 설치됨")
        except:
            report.append(f"[{name}] \t\t\t\t\t\t⚠️ 미설치 (해당 포맷 분석 불가)")
    report.append("PDF 분석 라이브러리(fitz) 로드 상태 : OK" if config.PDF_READY else "PDF 분석 라이브러리(fitz) 로드 상태 : No")
    report.append("Word 분석 라이브러리(docx) 로드 상태 : OK" if config.DOCX_READY else "Word 분석 라이브러리(docx) 로드 상태 : No")
    report.append("Excel 분석 라이브러리(openpyxl) 로드 상태 : OK" if config.EXCEL_READY else "Excel 분석 라이브러리(openpyxl) 로드 상태 : No")
    report.append("PPT 분석 라이브러리(pptx) 로드 상태 : OK" if config.PPT_READY else "PPT 분석 라이브러리(pptx) 로드 상태 : No")
    report.append("HWP 분석 라이브러리(olefile) 로드 상태 : OK" if config.HWP_READY else "HWP 분석 라이브러리(olefile) 로드 상태 : No")
    report.append("=" * 60)
    full_report = "\n".join(report)
    print(full_report)
    log_message("\n" + full_report, "DIAGNOSTIC")
    return full_report
# --------------------------------
# 파일 이동 함수 개선 (v17 - Expert Fix)
# [개선] move_file 함수 개선하여 파일 이동 시 중복 이름 처리 및 예외 처리 강화
# [개선] 이동 전 최종적으로 한 번 더 제외 체크 수행
# [개선] 파일명에서 날짜/시간 패턴 제거하여 깔끔한 이름으로 이동
# [개선] 목적지에 이미 파일이 존재할 경우, 최신 시간 패턴을 붙여 중복 방지
# [개선] 파일 이동 시 재시도 로직 추가하여 일시적인 파일 잠금 문제 해결
# [개선] 이동 성공 시 화면 출력 여부 결정 및 로그 파일에 이동 기록 저장
# [개선] 이동 실패 시 상세 오류 메시지 출력 및 로그 기록 강화
# --------------------------------
def move_file(source, dest_dir):
    """파일 이동 (중복 시 기존 시간 제거 후 최신 시간 1개만 유지)"""
    try:
        # [핵심] 이동 전 최종적으로 한 번 더 체크
        if is_excluded(source): return
        
        if source.name in config.EXCLUDE_LIST: return # 파일명 자체가 제외 리스트에 있는 경우 (안전망)

        if dest_dir.name in config.EXCLUDE_LIST: return # 대상 폴더명이 제외 리스트에 있는 경우 (안전망)
        # 1. 원본 파일명에서 지저분한 이전 시간 패턴 제거
        dest_dir.mkdir(parents=True, exist_ok=True) # 대상 폴더가 없으면 생성 (중간 폴더도 함께)
        clean_filename = cleaning_filename(source.stem) # 파일명에서 날짜/시간 패턴 제거
        dest = dest_dir / f"{clean_filename}{source.suffix}" # 최종 대상 경로 (날짜/시간 패턴 제거된 이름)

        # 2. 목적지에 이미 파일이 있다면 최신 시간 하나만 붙임
        if dest.exists():
            now = datetime.now().strftime("%H%M%S")
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
                if i < max_retries - 1: time.sleep(1)
                else: raise
    except Exception as e:
        msg = f"이동 오류 ({source.name}): {str(e)}"
        print(f"❌ {msg}")
        log_error(msg)
# --------------------------------
# 빈 폴더 마킹 함수 개선 (v17 - Expert Fix)
# [개선] mark_empty_folders 함수 개선하여 빈 폴더를 찾아 '_빈폴더' 마킹 추가
# [개선] 경로 전체를 체크하여 제외 폴더 내 파일 보호
# [개선] 빈 폴더 마킹 시 기존 이름이 날짜/시간 패턴으로 끝나는 경우, 패턴 제거 후 마킹하도록 개선
# [개선] 빈 폴더 마킹 시 이미 '_빈폴더'로 끝나는 경우는 건너뛰도록 개선
# [개선] 빈 폴더 마킹 시 이름이 숫자로 시작하고 '_'를 포함하는 경우는 원래 분류된 폴더로 간주하여 마킹에서 제외하도록 개선
# [개선] 빈 폴더 마킹 중 오류 발생 시 상세 오류 메시지 출력 및 로그 기록 강화
# --------------------------------
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
# --------------------------------
# 경로 유효성 검사 함수 추가 (v17 - Expert Fix)
# [개선] validate_path 함수 추가하여 입력된 경로의 유효성을 검사하도록 개선
# [개선] 경로가 존재하지 않거나 접근할 수 없는 경우 None을 반환하도록 개선
# [개선] 경로 검사 중 발생하는 오류는 상세히 로그에 기록하되, 시스템이 계속 작동하도록 예외 처리 강화
# --------------------------------
def validate_path(path_str):
    try:
        if not path_str: return None
        p = Path(path_str)
        return p if p.exists() else None
    except: return None
    """
    프로그램 시작 시 존재하던 폴더만 기억
    실행 중 새로 생성된 폴더는 무시하기 위한 용도
    """
    root = Path(root_path)
    folder_set = set()
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            current = current.resolve()
            folder_set.add(current)
            for item in current.iterdir():
                if item.is_dir():
                    # 제외 폴더 무시
                    if is_excluded(item): continue
                    stack.append(item)
        except Exception as e: log_error(f"폴더 구조 스캔 오류 ({current}): {e}")
    return folder_set

# --------------------------------
# 초기 폴더 기준 파일 탐색
# --------------------------------
def get_files_from_initial_folders(config.initial_folders):
    files = []
    for folder in config.initial_folders:
        try:
            for item in folder.iterdir():
                if item.is_file(): files.append(item)
        except Exception as e: log_error(f"파일 탐색 오류 ({folder}): {e}")
    return files

# --------------------------------
# 초기 폴더/파일 구조 기억
# Stack 기반 DFS
# --------------------------------
def build_initial_state(root_path):
    """
    프로그램 시작 시 존재하던
    폴더 + 파일 상태 기억

    새로 생성된 폴더/파일은
    이후 탐색 대상에서 제외
    """
    root = Path(root_path).resolve()
    folder_set = set()
    file_set = set()
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            current = current.resolve()
            # 폴더 기억
            folder_set.add(current)
            for item in current.iterdir():
                # 제외 목록
                if is_excluded(item):
                    continue
                if item.is_dir():
                    stack.append(item)
                elif item.is_file():
                    # 파일까지 기억
                    file_set.add(item.resolve())
        except Exception as e: log_error( f"초기 구조 스캔 오류 ({current}): {e}" )
    return folder_set, file_set

# --------------------------------
# 초기 상태 기준 파일 탐색
# --------------------------------
def get_initial_files(config.initial_folders, config.initial_files):
    result = []
    for folder in config.initial_folders:
        try:
            # 현재 폴더가 삭제되었을 수도 있음
            if not folder.exists(): continue
            for item in folder.iterdir():
                try:
                    item = item.resolve()
                    # 파일만
                    if not item.is_file(): continue
                    # 최초 상태 파일만 허용
                    if item not in config.initial_files: continue
                    result.append(item)
                except Exception: continue
        except Exception as e: log_error( f"초기 파일 탐색 오류 ({folder}): {e}" )
    return result

# --------------------------------
# 초기 폴더/파일 상태 기억
# Stack 기반 DFS
# --------------------------------
def build_initial_state(root_path):
    root = Path(root_path).resolve()
    config.initial_folders.clear()
    config.initial_files.clear()
    stack = [root]
    while stack:
        current = stack.pop()
        try:
            current = current.resolve()
            # 폴더 기억
            config.initial_folders.add(current)
            for item in current.iterdir():
                # 제외 경로
                if is_excluded(item): continue
                if item.is_dir(): stack.append(item)
                elif item.is_file():
                    config.initial_files.add( item.resolve() )
        except Exception as e: log_error( f"초기 상태 스캔 오류 ({current}): {e}" )

# --------------------------------
# 최초 상태 파일만 반환
# --------------------------------
def get_initial_files():
    result = []
    for folder in config.initial_folders:
        try:
            if not folder.exists(): continue
            for item in folder.iterdir():
                try:
                    item = item.resolve()
                    # 파일만
                    if not item.is_file(): continue
                    # 최초 상태 파일만
                    if item not in config.initial_files: continue
                    result.append(item)
                except Exception:   continue
        except Exception as e: log_error( f"초기 파일 탐색 오류 ({folder}): {e}" )
    return result