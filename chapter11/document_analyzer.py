from pathlib import Path

import config
import utils


def process(file_list: list[Path], result_base_path: Path) -> int:
    """문서 파일을 파일명 키워드 기준으로 분류 폴더에 이동합니다."""
    count = 0

    for file_path in file_list:
        if utils.should_skip(file_path):
            continue
        if file_path.suffix.lower() not in config.DOCUMENT_EXTENSIONS:
            continue

        lower_name = file_path.name.lower()
        matched_folder = config.DEFAULT_DOC_FOLDER

        for folder, keywords in config.KEYWORD_RULES.items():
            if any(keyword.lower() in lower_name for keyword in keywords):
                matched_folder = folder
                break

        moved = utils.move_file_safe(file_path, result_base_path / matched_folder)
        if moved != file_path:
            count += 1

    return count
