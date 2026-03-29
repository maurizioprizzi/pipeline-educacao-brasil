"""
Executa a pipeline completa de ponta a ponta.

Orquestra: ingestão → transformação → análise → visualização.
Idempotente: pode rodar várias vezes sem efeitos colaterais.
"""

import sys
import time
from datetime import datetime

from src.logger import get_logger

logger = get_logger("pipeline")


def run_full_pipeline():
    """Executa todas as etapas da pipeline com timing."""
    start = time.time()
    timestamp = datetime.now().isoformat()
    logger.info(f"{'='*60}")
    logger.info(f"PIPELINE INICIADA — {timestamp}")
    logger.info(f"{'='*60}")

    steps = [
        ("Ingestão IBGE", _step_ingest_ibge),
        ("Ingestão INEP", _step_ingest_inep),
        ("Transformação e carga", _step_transform),
        ("Análise", _step_analyze),
        ("Visualização", _step_visualize),
    ]

    results = []
    for name, func in steps:
        step_start = time.time()
        logger.info(f"--- {name} ---")
        try:
            func()
            elapsed = time.time() - step_start
            logger.info(f"OK: {name} ({elapsed:.1f}s)")
            results.append((name, "OK", elapsed))
        except Exception as e:
            elapsed = time.time() - step_start
            logger.error(f"FALHA: {name} — {e}")
            results.append((name, "FALHA", elapsed))

    total = time.time() - start
    logger.info(f"{'='*60}")
    logger.info(f"PIPELINE FINALIZADA — {total:.1f}s total")
    for name, status, elapsed in results:
        logger.info(f"  {status:5s} | {elapsed:6.1f}s | {name}")
    logger.info(f"{'='*60}")

    failed = [r for r in results if r[1] == "FALHA"]
    if failed:
        logger.error(f"{len(failed)} etapa(s) falharam")
        sys.exit(1)


def _step_ingest_ibge():
    from src.ingestion.extract import run_extraction
    run_extraction()


def _step_ingest_inep():
    from src.ingestion.extract_inep import run_inep_extraction
    run_inep_extraction()


def _step_transform():
    from src.transformation.run import run_transformation
    run_transformation()


def _step_analyze():
    from src.analysis.build_analytics import build_analytics
    build_analytics()


def _step_visualize():
    from src.visualization.run import run_visualization
    run_visualization()


if __name__ == "__main__":
    run_full_pipeline()