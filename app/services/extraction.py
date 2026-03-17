import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def extract_claims(text: str) -> Dict[str, Any]:
    """
    Extract factual claims from text.
    Modified to work offline: returns the entire text as a single claim.
    """
    logger.info(f"Extracting claims from: {text[:50]}...")
    
    # Simple offline pass-through logic
    if not text or not text.strip():
        return {"claims": []}
    
    return {"claims": [text.strip()]}
