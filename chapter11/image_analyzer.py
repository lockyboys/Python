from pathlib import Path

import config
import utils


def classify_by_filename(file_path: Path) -> str:
    """이미지 파일명을 보고 자연/도시/인물 계열 폴더를 선택합니다."""
    lower_name = file_path.name.lower()
    for folder, keywords in config.FILENAME_ROOM_RULES.items():
        if any(keyword.lower() in lower_name for keyword in keywords):
            return folder
    return config.DEFAULT_IMAGE_FOLDER


def process(image_pool: list[Path], result_base_path: Path) -> int:
    """이미지 파일을 파일명 규칙에 따라 분류 폴더로 이동합니다."""
    count = 0

    for file_path in image_pool:
        if utils.should_skip(file_path):
            continue
        if file_path.suffix.lower() not in config.IMAGE_EXTENSIONS:
            continue

        matched_folder = classify_by_filename(file_path)
        moved = utils.move_file_safe(file_path, result_base_path / matched_folder)
        if moved != file_path:
            count += 1

    return count
