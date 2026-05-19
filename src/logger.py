"""PDF转Word工具 - 日志模块"""

import logging
import os
from pathlib import Path
from datetime import datetime


def setup_logger(name="PDF转Word工具", log_dir=None, level=logging.INFO):
    """创建日志记录器，默认输出到桌面"""
    if log_dir is None:
        log_dir = Path(os.path.expanduser("~/Desktop"))

    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"{name}_{date_str}.log"

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setLevel(level)

    fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(fmt)
    logger.addHandler(console)

    return logger


def get_logger(name="PDF转Word工具"):
    """获取已创建的logger实例"""
    return logging.getLogger(name)