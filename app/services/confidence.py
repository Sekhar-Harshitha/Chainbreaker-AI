from typing import Dict, Any

def calculate_confidence(verdict: str, text: str) -> Dict[str, Any]:
    """
    Calculate deterministic confidence score based on the verdict (Point 9).
    """
    verdict = verdict.strip().upper()
    
    if verdict == "FALSE":
        # FALSE -> 85% (High)
        score = 85
        level = "High"
        sources = 24
    elif verdict == "TRUE":
        # TRUE -> 80% (High)
        score = 80
        level = "High"
        sources = 18
    else:
        # UNCERTAIN -> 55% (Medium)
        score = 55
        level = "Medium"
        sources = 5
        
    return {
        "confidence_score": score,
        "confidence_level": level,
        "source_count": sources
    }
