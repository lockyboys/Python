import gc
import logging
import shutil
import sys
from datetime import datetime
from pathlib import Path

import config

MOVED_FILES_REGISTRY = {}


def setup_logging_pipeline() -> None:
    """로그 파일과 콘솔 출력 파이프라인을 한 번만 초기화합니다."""
    if not config.LOG_FILE_YN:
        return

    log_dir = Path(config.BASE_LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    if logger.handlers:
        return

    if config.LOG_DATE_YN:
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{config.LOG_FILE_PREFIX}_{current_time}.log"
    else:
        filename = f"{config.LOG_FILE_PREFIX}.log"

    full_log_path = log_dir / filename
    config.LOG_FILE_NAME = str(full_log_path)

    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(config.LOG_FILE_NAME, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def log_message(msg: str) -> None:
    setup_logging_pipeline()
    logging.info(msg)


def log_error(msg: str, critical: bool = False) -> None:
    setup_logging_pipeline()
    if critical:
        logging.critical("[CRITICAL ERROR] %s", msg)
    else:
        logging.error("[ERROR] %s", msg)


def is_protected_zone(path: Path | str) -> bool:
    """Windows 시스템 경로처럼 건드리면 위험한 위치인지 확인합니다."""
    low_path = str(path).lower()
    return any(keyword in low_path for keyword in config.SYSTEM_PROTECTED_KEYWORDS)


def should_skip(path: Path) -> bool:
    """이미 이동했거나 제외 대상인 파일은 다시 처리하지 않도록 거릅니다."""
    if not path.exists():
        return True
    if path.name in config.EXCLUDE_LIST:
        return True
    if is_protected_zone(path):
        return True
    if str(path) in MOVED_FILES_REGISTRY or path in MOVED_FILES_REGISTRY.values():
        return True
    return False


def unique_destination(source_file: Path, target_folder: Path) -> Path:
    """대상 폴더에 같은 이름이 있으면 _1, _2를 붙인 안전한 경로를 만듭니다."""
    destination_path = target_folder / source_file.name
    if not destination_path.exists():
        return destination_path

    if source_file.stat().st_size == destination_path.stat().st_size:
        return destination_path

    idx = 1
    while True:
        destination_path = target_folder / f"{source_file.stem}_{idx}{source_file.suffix}"
        if not destination_path.exists():
            return destination_path
        idx += 1


def move_file_safe(source_file: Path, target_folder: Path) -> Path:
    """파일 이동을 수행하고, 실패하면 복사 후 원본 삭제 방식으로 한 번 더 시도합니다."""
    if not source_file.exists():
        return source_file

    target_folder.mkdir(parents=True, exist_ok=True)
    destination_path = unique_destination(source_file, target_folder)

    if destination_path.exists() and source_file.stat().st_size == destination_path.stat().st_size:
        log_message(f"[중복 삭제] 같은 크기의 파일이 이미 있음: {source_file.name}")
        try:
            source_file.unlink()
        except OSError as exc:
            log_error(f"중복 파일 삭제 실패 [{source_file.name}] - {exc}")
        return destination_path

    for attempt in range(1, 4):
        try:
            gc.collect()
            shutil.move(str(source_file), str(destination_path))
            MOVED_FILES_REGISTRY[str(source_file)] = destination_path
            log_message(f"[이동 성공] {source_file.name} -> {target_folder.name}")
            return destination_path
        except OSError as exc:
            if attempt < 3:
                continue
            try:
                shutil.copy2(str(source_file), str(destination_path))
                source_file.unlink()
                MOVED_FILES_REGISTRY[str(source_file)] = destination_path
                log_message(f"[복사 후 삭제] {source_file.name} -> {target_folder.name}")
                return destination_path
            except OSError as copy_exc:
                log_error(f"파일 이동 실패 [{source_file.name}] - {exc} / {copy_exc}")
                return source_file


def target_folder_by_extension(file_path: Path) -> str:
    """확장자 기준으로 파일이 들어갈 기본 분류 폴더를 반환합니다."""
    ext = file_path.suffix.lower()
    for folder, extensions in config.EXTENSION_RULES.items():
        if ext in extensions:
            return folder
    return config.DEFAULT_OTHER_FOLDER


def dispatch_file_to_isolation(source_file: Path, base_isolation_path: Path) -> Path:
    """하위 폴더 파일을 원본 격리 폴더 안의 종류별 폴더로 보냅니다."""
    folder = target_folder_by_extension(source_file)
    return move_file_safe(source_file, base_isolation_path / folder)


def collect_target_files_recursively(root_dir: Path, result_base_path: Path) -> list[Path]:
    """정리 대상 폴더에서 처리할 파일만 재귀적으로 수집합니다."""
    collected = []
    ignored_parts = {
        config.RESULT_FOLDER_NAME,
        config.ISOLATION_FOLDER_NAME,
        "Logs",
    }

    for path in root_dir.rglob("*"):
        if not path.is_file():
            continue
        if any(part in ignored_parts for part in path.parts):
            continue
        if should_skip(path):
            continue
        try:
            path.relative_to(result_base_path)
            continue
        except ValueError:
            pass
        collected.append(path)

    return collected
