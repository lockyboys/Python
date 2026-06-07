from pathlib import Path

import config
import utils


def process(file_list: list[Path], result_base_path: Path) -> int:
    """영상 파일을 기본 영상 폴더로 이동합니다."""
    count = 0

    for file_path in file_list:
        if utils.should_skip(file_path):
            continue
        if file_path.suffix.lower() not in config.VIDEO_EXTENSIONS:
            continue

        moved = utils.move_file_safe(file_path, result_base_path / config.DEFAULT_VIDEO_FOLDER)
        if moved != file_path:
            count += 1

    return count
