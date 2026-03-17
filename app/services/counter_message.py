import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Basic Tamil/Hindi word samples for language detection
TAMIL_WORDS = {"இது", "உண்மை", "தகவல்", "பகிர", "நோய்", "மருந்து", "அரசு", "டாக்டர்"}
HINDI_WORDS = {"यह", "सच", "जानकारी", "शेयर", "बीमारी", "दवा", "सरकार", "डॉक्टर"}

# Counter-messages by language
COUNTER_MESSAGES = {
    "tamil": "⚠️ இந்த தகவல் தவறானது. தயவுசெய்து உறுதிப்படுத்தப்படாத செய்திகளை பகிர வேண்டாம்.",
    "hindi": "⚠️ यह जानकारी गलत है। कृपया बिना जाँचे संदेश को आगे न बढ़ाएं।",
    "english": "⚠️ This information is false. Please avoid sharing unverified messages.",
}

def _detect_language(text: str) -> str:
    words = set(text.split())
    if words & TAMIL_WORDS:
        return "tamil"
    if words & HINDI_WORDS:
        return "hindi"
    return "english"

def generate_counter_message(text: str, verdict: str) -> Optional[str]:
    """
    Generate a short, corrective WhatsApp message for FALSE claims.
    """
    if verdict.upper() != "FALSE":
        return None

    language = _detect_language(text)
    message = COUNTER_MESSAGES[language]

    logger.info(f"Counter message generated ({language}): {message}")
    return message
