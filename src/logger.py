"""
Configuração de logging centralizada.

Uso:
    from src.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Ingestão iniciada")
"""

import logging
import sys

from src.config import LOG_FORMAT, LOG_DATE_FORMAT


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Cria um logger configurado para o módulo especificado."""
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(level)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        logger.propagate = False

    return logger