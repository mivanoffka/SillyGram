import logging
import tarfile
from datetime import datetime, timedelta
from ..context import PATH
from pathlib import Path
import colorlog


class SillyLogger:
    class Mode:
        ALL = 10
        DEBUG = 10
        INFO = 20
        WARNING = 30
        ERROR = 40
        CRITICAL = 50
        DISABLED = 9999

    _file_logging_mode: Mode
    _console_logging_mode: Mode

    def __init__(
        self,
        path: str | Path,
        file_logging_mode: Mode,
        console_logging_mode: Mode,
    ):
        self.folder_name = Path(path) if Path(path).is_absolute() else PATH / path
        self._file_logging_mode = file_logging_mode
        self._console_logging_mode = console_logging_mode

        self._archive_old_logs()
        self._rotate_log_file()

    @property
    def log_folder(self):
        log_folder = PATH / self.folder_name / datetime.now().strftime("%Y-%m-%d")
        if not log_folder.exists():
            log_folder.mkdir(parents=True)
        return log_folder

    def _rotate_log_file(self):
        current_log_folder = self.log_folder
        current_log_file = current_log_folder / datetime.now().strftime("%H-%M-%S.log")

        if current_log_file.exists():
            return

        logger = logging.getLogger()
        logger.setLevel(SillyLogger.Mode.ALL)

        file_handler = logging.FileHandler(current_log_file)
        file_handler.setLevel(self._file_logging_mode)
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - [%(levelname)s] - %(funcName)s - %(message)s"
            )
        )
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(self._console_logging_mode)

        color_formatter = colorlog.ColoredFormatter(
            "%(log_color)s%(asctime)s - [%(levelname)s] - %(funcName)s - %(message)s",
            datefmt=None,
            reset=True,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "white",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )

        console_handler.setFormatter(color_formatter)
        logger.addHandler(console_handler)

    def _archive_old_logs(self, days: int = 7):
        old_logs_time = datetime.now() - timedelta(days=days)
        logs_folder = self.log_folder

        for log_folder in logs_folder.iterdir():
            if (
                log_folder.is_dir()
                and datetime.strptime(log_folder.name, "%Y-%m-%d") < old_logs_time
            ):
                archive_path = log_folder.with_suffix(".tar.gz")
                with tarfile.open(archive_path, "w:gz") as archive:
                    archive.add(log_folder, arcname=log_folder.name)
                for log_file in log_folder.iterdir():
                    log_file.unlink()
                log_folder.rmdir()
