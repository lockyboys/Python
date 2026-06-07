import argparse
import shutil
from pathlib import Path

import audio_analyzer
import config
import dashboard
import document_analyzer
import image_analyzer
import utils
import video_analyzer


def build_base_folders(target_path: Path, result_base_path: Path) -> None:
    """사용자가 결과 구조를 바로 볼 수 있도록 기본 폴더와 안내 파일을 만듭니다."""
    for folder_name in config.PRE_BUILD_FOLDERS:
        (target_path / folder_name).mkdir(parents=True, exist_ok=True)
        (result_base_path / folder_name).mkdir(parents=True, exist_ok=True)

    for target_folder, file_names in config.PRE_BUILD_FILES.items():
        for file_name in file_names:
            for base_path in (target_path, result_base_path):
                file_path = base_path / target_folder / file_name
                if file_path.exists():
                    utils.MOVED_FILES_REGISTRY[str(file_path)] = file_path
                    continue
                file_path.write_text(
                    "이 파일은 정리 폴더 안내용으로 자동 생성되었습니다.\n",
                    encoding="utf-8",
                )
                utils.MOVED_FILES_REGISTRY[str(file_path)] = file_path


def isolate_subfolder_files(target_path: Path, isolation_zone: Path) -> int:
    """하위 폴더 안의 파일을 원본 격리 폴더로 먼저 모읍니다."""
    moved_count = 0
    ignored_names = {
        config.RESULT_FOLDER_NAME,
        config.ISOLATION_FOLDER_NAME,
        "Logs",
        *config.PRE_BUILD_FOLDERS,
    }

    subfolders = [
        path
        for path in target_path.iterdir()
        if path.is_dir() and path.name not in ignored_names and not utils.is_protected_zone(path)
    ]

    for subfolder in subfolders:
        for item in list(subfolder.rglob("*")):
            if not item.is_file() or utils.should_skip(item):
                continue
            moved = utils.dispatch_file_to_isolation(item, isolation_zone)
            if moved != item:
                moved_count += 1

        if subfolder.exists() and not any(subfolder.iterdir()):
            archive_name = subfolder.name
            if not archive_name.endswith("_빈폴더"):
                archive_name = f"{archive_name}_빈폴더"
            destination = isolation_zone / archive_name
            destination.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.move(str(subfolder), str(destination))
            except OSError as exc:
                utils.log_error(f"빈 폴더 격리 실패 [{subfolder.name}] - {exc}")

    return moved_count


def extension_sweep(file_pool: list[Path], result_base_path: Path) -> int:
    """전문 분석기에 걸리지 않은 나머지 파일을 확장자 기준으로 정리합니다."""
    count = 0
    for file_path in file_pool:
        if utils.should_skip(file_path):
            continue
        folder = utils.target_folder_by_extension(file_path)
        moved = utils.move_file_safe(file_path, result_base_path / folder)
        if moved != file_path:
            count += 1
    return count


def organize(
    target_path: Path,
    unpack_all: bool = True,
    make_dashboard: bool = True,
) -> dict[str, int | str]:
    """전체 정리 작업의 메인 흐름입니다."""
    target_path = target_path.expanduser().resolve()

    if not target_path.exists() or not target_path.is_dir():
        raise FileNotFoundError(f"정리 대상 폴더가 없습니다: {target_path}")
    if utils.is_protected_zone(target_path):
        raise PermissionError(f"보호 경로는 정리할 수 없습니다: {target_path}")

    result_base_path = target_path / config.RESULT_FOLDER_NAME
    isolation_zone = target_path / config.ISOLATION_FOLDER_NAME
    config.BASE_LOG_DIR = str(target_path / "Logs")

    utils.log_message("=" * 70)
    utils.log_message(f"{config.APP_NAME} 시작: {target_path}")
    utils.log_message("=" * 70)

    isolation_count = 0
    if unpack_all:
        isolation_zone.mkdir(parents=True, exist_ok=True)
        isolation_count = isolate_subfolder_files(target_path, isolation_zone)

    build_base_folders(target_path, result_base_path)

    # 1차 수집 후 파일 종류별 분석기로 나누어 처리합니다.
    files = utils.collect_target_files_recursively(target_path, result_base_path)

    video_pool = [file for file in files if file.suffix.lower() in config.VIDEO_EXTENSIONS]
    document_pool = [file for file in files if file.suffix.lower() in config.DOCUMENT_EXTENSIONS]
    image_pool = [file for file in files if file.suffix.lower() in config.IMAGE_EXTENSIONS]
    audio_pool = [file for file in files if file.suffix.lower() in config.AUDIO_EXTENSIONS]

    result: dict[str, int | str] = {
        "isolated": isolation_count,
        "videos": video_analyzer.process(video_pool, result_base_path),
        "documents": document_analyzer.process(document_pool, result_base_path),
        "images": image_analyzer.process(image_pool, result_base_path),
        "audio": audio_analyzer.process(audio_pool, result_base_path),
    }

    # 분석기에서 처리되지 않은 파일을 마지막으로 한 번 더 정리합니다.
    remaining_files = utils.collect_target_files_recursively(target_path, result_base_path)
    result["other"] = extension_sweep(remaining_files, result_base_path)

    if make_dashboard:
        dashboard_path = dashboard.generate_dashboard(
            target_path,
            result_base_path,
            {key: int(value) for key, value in result.items() if isinstance(value, int)},
        )
        result["dashboard"] = str(dashboard_path)

    utils.log_message("-" * 50)
    utils.log_message(f"격리 보관: {result['isolated']}개")
    utils.log_message(f"영상 정리: {result['videos']}개")
    utils.log_message(f"문서 정리: {result['documents']}개")
    utils.log_message(f"이미지 정리: {result['images']}개")
    utils.log_message(f"오디오 정리: {result['audio']}개")
    utils.log_message(f"기타 정리: {result['other']}개")
    if make_dashboard:
        utils.log_message(f"대시보드 생성: {result['dashboard']}")
    utils.log_message(f"완료: {target_path}")
    return result


def parse_args() -> argparse.Namespace:
    """명령줄 인자를 읽어서 실행 대상 폴더와 옵션을 가져옵니다."""
    parser = argparse.ArgumentParser(description="파일을 종류별 폴더로 정리합니다.")
    parser.add_argument("target", nargs="?", help="정리할 폴더 경로")
    parser.add_argument(
        "--keep-subfolders",
        action="store_true",
        help="하위 폴더를 원본 격리 폴더로 옮기지 않고 현재 위치의 파일만 정리합니다.",
    )
    parser.add_argument(
        "--no-dashboard",
        action="store_true",
        help="정리 완료 후 dashboard.html을 만들지 않습니다.",
    )
    return parser.parse_args()


def main() -> None:
    """명령줄 실행 진입점입니다."""
    args = parse_args()
    target = args.target

    if not target:
        print("정리할 폴더 경로를 입력하세요.")
        target = input("경로: ").strip().strip('"')

    if not target:
        print("경로가 입력되지 않아 종료합니다.")
        return

    try:
        result = organize(
            Path(target),
            unpack_all=not args.keep_subfolders,
            make_dashboard=not args.no_dashboard,
        )
    except Exception as exc:
        utils.log_error(str(exc), critical=True)
        print(f"실패: {exc}")
        return

    print("\n정리 완료")
    for key, value in result.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
