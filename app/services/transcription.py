import logging

logger = logging.getLogger(__name__)

async def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio file.
    Modified to work offline: returns a placeholder message.
    """
    logger.info(f"Transcribing audio file: {file_path}")
    
    # Placeholder for offline transcription
    return "This is an offline placeholder transcription. Local transcription models are not currently configured."
