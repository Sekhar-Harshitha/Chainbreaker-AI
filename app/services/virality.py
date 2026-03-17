import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def calculate_virality_score(text: str) -> Dict[str, Any]:
    """
    Calculate a virality score (1-10) based on textual triggers (Point 8).
    """
    score = 1
    text_lower = text.lower()
    
    # +3 -> urgent words
    urgent_words = ["urgent", "hurry", "immediately", "asap", "warning", "emergency", "100%"]
    if any(word in text_lower for word in urgent_words):
        score += 3
        
    # +2 -> emotional words
    emotional_words = ["shocking", "amazing", "heartbreaking", "unbelievable", "horrible", "scary", "miracle"]
    if any(word in text_lower for word in emotional_words):
        score += 2
        
    # +2 -> “forward” / share trigger
    share_triggers = ["forward", "share", "tell everyone", "dont keep this", "repost", "forward now"]
    if any(word in text_lower for word in share_triggers):
        score += 2
        
    # +3 -> medical claims
    medical_words = ["cure", "vaccine", "doctor", "health", "cancer", "treatment", "medicine", "pill"]
    if any(word in text_lower for word in medical_words):
        score += 3
        
    # Clamp to 1-10
    final_score = max(1, min(10, score))
    
    logger.info(f"Calculated virality score: {final_score}")
    
    return {
        "score": final_score,
        "level": "High" if final_score >= 7 else "Medium" if final_score >= 4 else "Low"
    }
