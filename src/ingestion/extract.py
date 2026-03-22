"""
Módulo de extração de dados das APIs públicas.

Faz requests com retry e salva os dados brutos em data/raw/.
"""

import json
import time
from datetime import datetime

import requests

from src.config import SOURCES, RAW_DIR, REQUEST_TIMEOUT, REQUEST_RETRIES
from src.logger import get_logger

logger = get_logger(__name__)


def fetch_source(name: str, source: dict) -> dict | None:
    """Faz GET na API com retries. Retorna o JSON ou None se falhar."""
    url = source["url"]

    for attempt in range(1, REQUEST_RETRIES + 1):
        try:
            logger.info(f"[{name}] Tentativa {attempt}/{REQUEST_RETRIES} — {url}")
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            data = response.json()

            if not data:
                logger.warning(f"[{name}] API retornou dados vazios")
                return None

            logger.info(f"[{name}] OK — {len(response.text)} bytes recebidos")
            return data

        except requests.exceptions.HTTPError as e:
            logger.error(f"[{name}] Erro HTTP: {e}")
        except requests.exceptions.ConnectionError:
            logger.error(f"[{name}] Erro de conexão")
        except requests.exceptions.Timeout:
            logger.error(f"[{name}] Timeout após {REQUEST_TIMEOUT}s")
        except requests.exceptions.JSONDecodeError:
            logger.error(f"[{name}] Resposta não é JSON válido")

        if attempt < REQUEST_RETRIES:
            wait = attempt * 2
            logger.info(f"[{name}] Aguardando {wait}s antes de tentar novamente...")
            time.sleep(wait)

    logger.error(f"[{name}] Falhou após {REQUEST_RETRIES} tentativas")
    return None


def save_raw(name: str, data: dict) -> None:
    """Salva o JSON bruto em data/raw/ com timestamp."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    filepath = RAW_DIR / f"{name}.json"
    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"[{name}] Salvo em {filepath}")


def run_extraction() -> dict:
    """Executa a extração de todas as fontes. Retorna resumo."""
    timestamp = datetime.now().isoformat()
    logger.info(f"Início da ingestão — {timestamp}")

    results = {"ok": [], "falha": []}

    for name, source in SOURCES.items():
        logger.info(f"--- {source['description']} ---")
        data = fetch_source(name, source)

        if data:
            save_raw(name, data)
            results["ok"].append(name)
        else:
            results["falha"].append(name)

    logger.info(f"Ingestão finalizada — OK: {len(results['ok'])}, Falhas: {len(results['falha'])}")
    return results