# [document_analyzer.py] - 문서 분석 모듈 (v15 - Robust Error Handling)
import os
import config
import utils
from pathlib import Path

PDF_READY = False
DOCX_READY = False
EXCEL_READY = False
PPT_READY = False
HWP_READY = False

try:
    import fitz
    PDF_READY = True
except Exception as e: utils.log_error(f"PDF 라이브러리 로드 실패: {e}", False)

try:
    from docx import Document
    DOCX_READY = True
except Exception as e: utils.log_error(f"Word 라이브러리 로드 실패: {e}", False)

try:
    import openpyxl
    EXCEL_READY = True
except Exception as e: utils.log_error(f"Excel 라이브러리 로드 실패: {e}", False)

try:
    from pptx import Presentation
    PPT_READY = True
except Exception as e: utils.log_error(f"PPT 라이브러리 로드 실패: {e}", False)

try:
    import olefile
    HWP_READY = True
except Exception as e: utils.log_error(f"HWP 라이브러리 로드 실패: {e}", False)

def extract_text(file_path):
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
            text = " ".join([str(c) for row in wb.active.iter_rows(max_row=50, values_only=True) for c in row if c])
        elif ext in [".pptx", ".ppt"] and PPT_READY:
            prs = Presentation(file_path)
            for slide in prs.slides[:10]:
                for shape in slide.shapes:
                    if hasattr(shape, "text"): text += shape.text + " "
        elif ext in [".hwp", ".hwpx"] and HWP_READY:
            f = olefile.OleFileIO(file_path)
            if 'PrvText' in f.listdir():
                text = f.openstream('PrvText').read().decode('utf-16', errors='ignore')
            f.close()
    except Exception as e:
        utils.log_error(f"문서 텍스트 추출 오류 ({file_path.name}): {e}")
    return text[:config.MAX_DOC_TEXT_LENGTH]

def analyze_document_content(file_path):
    try:
        name = file_path.name.lower()
        for folder, kws in config.KEYWORD_RULES.items():
            if any(kw.lower() in name for kw in kws): return folder
        content = extract_text(file_path).lower()
        if content:
            for folder, kws in config.KEYWORD_RULES.items():
                if any(kw.lower() in content for kw in kws): return folder
        for folder, exts in config.EXTENSION_RULES.items():
            if file_path.suffix.lower() in exts: return folder
    except Exception as e:
        utils.log_error(f"문서 내용 분석 오류 ({file_path.name}): {e}")
    return "99_미분류_기타"

def run_document_organizing(target_path):
    target = Path(target_path)
    count = 0
    print("📄 문서 내용 분석 엔진 가동 중...")
    try:
        search_pattern = '**/*' if config.RECURSIVE_SCAN else '*'
        doc_files = [f for f in target.glob(search_pattern) if f.is_file() and f.suffix.lower() in config.DOCUMENT_EXTENSIONS]
        for item in doc_files:
            if any(p.name.startswith(('0', '1', 'AI_TF', '영상_그룹', 'Group_')) for p in item.parents if p != target):
                continue
            category = analyze_document_content(item)
            utils.move_file(item, target / category)
            count += 1
    except Exception as e:
        utils.log_error(f"문서 정리 프로세스 오류: {e}")
    return count
