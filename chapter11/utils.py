# [utils.py] - 공통 도구 함수
import os
import shutil
from pathlib import Path

def move_file(source, dest_dir):
    """파일을 안전하게 이동 (이름 중복 시 자동 변경)"""
    # parents=True 옵션을 추가하여 상위 폴더가 없으면 한꺼번에 생성하도록 수정했습니다.
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / source.name
    if dest.exists():
        dest = dest_dir / f"{source.stem}_{int(os.path.getmtime(source))}{source.suffix}"
    shutil.move(str(source), str(dest))
    print(f"✅ {source.name} -> {dest_dir.name}/")

def validate_path(path_str):
    """경로 유효성 검사"""
    p = Path(path_str)
    return p if p.exists() else None
