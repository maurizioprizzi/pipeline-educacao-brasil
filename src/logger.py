"""
Configuração de logging centralizada.

Logs vão para stdout (terminal) e para arquivo (logs/pipeline.log).

Uso:
    from src.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Ingestão iniciada")
"""

import logging
import sys
from pathlib import Path

from src.config import LOG_FORMAT, LOG_DATE_FORMAT, ROOT_DIR

LOG_DIR = ROOT_DIR / "logs"


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Cria um logger que escreve no terminal e em arquivo."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)
        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

        # Terminal
        console = logging.StreamHandler(sys.stdout)
        console.setLevel(level)
        console.setFormatter(formatter)
        logger.addHandler(console)

        # Arquivo
        LOG_DIR.mkdir(exist_ok=True)
        file_handler = logging.FileHandler(
            LOG_DIR / "pipeline.log", encoding="utf-8"
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        logger.propagate = False

    return logger