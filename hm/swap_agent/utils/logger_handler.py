from datetime import datetime
import logging
import os

from utils.path_tools import get_abs_path

# 日志保存的根目录
LOG_ROOT_DIR = get_abs_path("logs")

os.makedirs(LOG_ROOT_DIR, exist_ok=True)

# 日志格式
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# 创建日志处理器
def get_logger(
    name: str = "swap_agent",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    log_file: str = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加处理器
    if logger.handlers:
        return logger

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    # 创建文件处理器
    if not log_file:
        log_file = os.path.join(LOG_ROOT_DIR, f"{name}_{datetime.now().strftime('%Y-%m-%d')}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)
    return logger


# 快捷获取日志记录器
logger = get_logger()


if __name__ == "__main__":
    logger.info("test")
    logger.debug("test")
    logger.warning("test")
    logger.error("test")
    logger.critical("test")
