import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

async def generate_response(transcription: str, claims: List[str], fact_check_results: List[Dict[str, Any]]) -> str:
    """
    Generate a WhatsApp-friendly response based on the transcription, extracted claims, and fact-checking results.
    Modified to work offline: uses predefined templates.
    """
    if not claims or not fact_check_results:
        return "There were no verifiable claims in your message for me to check. Please send a factual statement!"

    # Get the overall verdict
    has_false = any(r.get('verdict') == 'false' for r in fact_check_results)
    
    summary = f"I analyzed your message: \"{transcription[:50]}{'...' if len(transcription) > 50 else ''}\""
    
    if has_false:
        verdict_str = "❌ FALSE"
        explanation = "I found some high-risk keywords associated with known misinformation patterns."
    else:
        verdict_str = "❓ UNCERTAIN"
        explanation = "I couldn't find any common misinformation triggers, but I cannot verify the exact facts offline."

    # Construct the response
    response = f"📝 Summary: {summary}\n\n"
    response += f"⚖️ Verdict: {verdict_str}\n\n"
    response += f"🔍 Explanation: {explanation}\n\n"
    
    if has_false:
        response += "Be careful with such information and always verify from official sources before sharing."
    else:
        response += "Please use your judgment and double-check this information."

    return response
