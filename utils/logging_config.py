import logging
import os
from logging.handlers import TimedRotatingFileHandler


def setup_logger(
    name: str = "readme_agent",
    log_dir: str = "./logs",
    level: int = logging.INFO,
) -> logging.Logger:

    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{name}.log")

    # Logger 생성
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # root logger로 중복 출력 방지

    # 이미 핸들러가 붙어있으면 재생성 방지
    if logger.handlers:
        return logger

    # 1) 콘솔 출력 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(
        logging.Formatter("[%(levelname)s] %(message)s")
    )

    # 2) 파일 핸들러 (매일 자동 rotate)
    file_handler = TimedRotatingFileHandler(
        filename=log_path,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
