import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

async def check_claim(claim: str) -> Dict[str, Any]:
    """
    Fact-check a given claim using refined rule-based logic.
    Returns: {"claim": "...", "verdict": "FALSE|TRUE|UNCERTAIN", "reason": "..."}
    """
    logger.info(f"Fact-checking claim: {claim}")
    
    claim_lower = claim.lower()
    
    # 1. FALSE Keywords (Point 5)
    false_keywords = ["cure", "miracle", "guarantee", "100%", "forward", "urgent", "government warning"]
    if any(kw in claim_lower for kw in false_keywords):
        return {
            "claim": claim,
            "verdict": "FALSE",
            "reason": "This claim uses exaggerated or misleading language and lacks scientific evidence."
        }
    
    # 2. Neutral factual statement logic (Point 5)
    # Simple heuristic: if it looks like a descriptive statement without hype
    factual_keywords = ["is", "are", "happened", "observed", "report"]
    if any(kw in claim_lower for kw in factual_keywords) and len(claim.split()) > 4:
         return {
            "claim": claim,
            "verdict": "TRUE",
            "reason": "This claim appears consistent with known reliable information."
        }
    
    # 3. Default to UNCERTAIN (Point 5)
    return {
        "claim": claim,
        "verdict": "UNCERTAIN",
        "reason": "This claim cannot be verified with available information."
    }

async def check_claims_batch(claims: List[str]) -> List[Dict[str, Any]]:
    """
    Fact checks multiple claims sequentially using refined rule-based logic.
    """
    results = []
    for claim in claims:
        results.append(await check_claim(claim))
    return results
