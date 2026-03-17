import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# In-memory cache: key = normalized claim text, value = result dict
cache: Dict[str, Dict[str, Any]] = {}


def normalize_text(text: str) -> str:
    """
    Normalize text for cache key lookup:
    - Lowercase
    - Strip and collapse extra whitespace
    """
    return " ".join(text.lower().split())


def get_cached_result(text: str) -> Optional[Dict[str, Any]]:
    """
    Return cached result for normalized text if it exists, else None.
    """
    key = normalize_text(text)
    result = cache.get(key)
    if result:
        logger.info(f"CACHE HIT for key: '{key}'")
        print(f"CACHE HIT: '{key}'")
    else:
        logger.info(f"CACHE MISS for key: '{key}'")
        print(f"CACHE MISS: '{key}'")
    return result


def store_result(text: str, result: Dict[str, Any]) -> None:
    """
    Store the processed result in cache under the normalized text key.
    """
    key = normalize_text(text)
    cache[key] = result
    logger.info(f"Stored result in cache for key: '{key}'")
