# [document_analyzer.py] - 다양한 문서 포맷 텍스트 추출 및 내용 분석 모듈 (v14)
import os
import config
import utils
from pathlib import Path

# --- 라이브러리 연결 (오류 방지용 예외 처리) ---
PDF_READY = False
DOCX_READY = False
EXCEL_READY = False
PPT_READY = False
HWP_READY = False

try:
    import fitz  # PyMuPDF
    PDF_READY = True
except ImportError: pass

try:
    from docx import Document
    DOCX_READY = True
except ImportError: pass

try:
    import openpyxl
    EXCEL_READY = True
except ImportError: pass

try:
    from pptx import Presentation
    PPT_READY = True
except ImportError: pass

try:
    import olefile
    HWP_READY = True
except ImportError: pass

def extract_text(file_path):
    """파일 확장자에 따라 텍스트를 추출합니다."""
    ext = file_path.suffix.lower()
    text = ""
    
    try:
        if ext == ".txt":
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read(config.MAX_DOC_TEXT_LENGTH)
        
        elif ext == ".pdf" and PDF_READY:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
                if len(text) > config.MAX_DOC_TEXT_LENGTH: break
            doc.close()
            
        elif ext in [".docx", ".doc"] and DOCX_READY:
            doc = Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs[:50]])
            
        elif ext in [".xlsx", ".xls"] and EXCEL_READY:
            wb = openpyxl.load_workbook(file_path, data_only=True, read_only=True)
            ws = wb.active
            for row in ws.iter_rows(max_row=50, values_only=True):
                text += " ".join([str(c) for c in row if c]) + " "
            
        elif ext in [".pptx", ".ppt"] and PPT_READY:
            prs = Presentation(file_path)
            for slide in prs.slides[:10]:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + " "
        
        elif ext in [".hwp", ".hwpx"] and HWP_READY:
            # HWP는 OLE 구조이므로 olefile로 텍스트 스트림 접근
            f = olefile.OleFileIO(file_path)
            if 'PrvText' in f.listdir():
                text = f.openstream('PrvText').read().decode('utf-16', errors='ignore')
            f.close()
            
    except Exception as e:
        utils.log_error(f"문서 텍스트 추출 실패 ({file_path.name}): {e}")
        
    return text[:config.MAX_DOC_TEXT_LENGTH]

def analyze_document_content(file_path):
    """문서 내용을 읽어 config의 키워드 규칙에 따라 분류를 결정합니다."""
    # 1. 파일명 우선 확인
    name = file_path.name.lower()
    for folder, kws in config.KEYWORD_RULES.items():
        if any(kw.lower() in name for kw in kws):
            return folder
            
    # 2. 내용 분석
    content = extract_text(file_path).lower()
    if content:
        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw.lower() in content for kw in kws):
                return folder
                
    # 3. 분류되지 않은 경우 확장자 기반 기본 폴더
    for folder, exts in config.EXTENSION_RULES.items():
        if file_path.suffix.lower() in exts:
            return folder
            
    return "99_미분류_기타"

def run_document_organizing(target_path):
    """메인 컨트롤러에서 호출하는 실행 함수"""
    target = Path(target_path)
    count = 0
    
    print("📄 지능형 문서 내용 분석 엔진 가동 중...")
    
    doc_files = [f for f in target.rglob('*') if f.is_file() and f.suffix.lower() in config.DOCUMENT_EXTENSIONS]
    
    for item in doc_files:
        # 이미 분류된 폴더 안에 있는 경우 제외
        if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹')) for p in item.parents if p != target):
            continue
            
        category = analyze_document_content(item)
        dest_folder = target / category
        utils.move_file(item, dest_folder)
        count += 1
        
    return count
