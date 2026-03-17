import os
import httpx
import json
import datetime
import logging
from pathlib import Path
from fastapi import APIRouter, Request, BackgroundTasks, Form
from fastapi.responses import Response
from typing import Optional
from twilio.rest import Client

from app.core.config import get_settings
from app.services.transcription import transcribe_audio
from app.services.extraction import extract_claims
from app.services.fact_check import check_claims_batch
from app.services.virality import calculate_virality_score
from app.services.cache import normalize_text, get_cached_result, store_result
from app.services.counter_message import generate_counter_message
from app.services.confidence import calculate_confidence

# Point 2: Add Logger
logger = logging.getLogger(__name__)

router = APIRouter()
settings = get_settings()

DATA_LOG_FILE = Path("data.json")

def log_pipeline_result(result: dict):
    """Log result to data.json for the dashboard."""
    try:
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            **result
        }
        with open(DATA_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        logger.error(f"Error logging result: {e}")

async def download_media(media_url: str, auth_tuple: tuple) -> str:
    """Download media from Twilio to a local temporary file."""
    file_path = "temp_audio.ogg" # Point 4: Save as temp_audio.ogg
    async with httpx.AsyncClient() as client:
        response = await client.get(media_url, auth=auth_tuple)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
    return file_path

async def process_whatsapp_message(
    sender: str, 
    body: str, 
    media_url: Optional[str] = None
):
    """Full pipeline for processing WhatsApp messages."""
    transcription = body
    cached = False
    
    try:
        # 1. Handle Audio (Point 4)
        if media_url:
            try:
                auth = (settings.twilio_account_sid, settings.twilio_auth_token)
                audio_path = await download_media(media_url, auth)
                transcription = await transcribe_audio(audio_path)
                logger.info("Audio detected → using transcription")
                if os.path.exists(audio_path):
                    os.remove(audio_path)
            except Exception as audio_err:
                logger.error(f"Audio processing failed, falling back to text: {audio_err}")
                # transcription remains as body (Point 12: Fail-safe)

        # 2. Cache Check (Deterministic now, but keeping for stability)
        normalized = normalize_text(transcription)
        cached_result = get_cached_result(normalized)
        
        if cached_result:
            verdict = cached_result.get("verdict")
            explanation = cached_result.get("explanation")
            virality_score = cached_result.get("virality_score")
            counter_message = cached_result.get("counter_message")
            cached = True
        else:
            # 3. Viral Score (Point 8)
            virality_result = calculate_virality_score(transcription)
            virality_score = virality_result["score"]
            
            # 4. Extraction & Fact Check (Point 5 & 6 & 7)
            # Simplified flow for deterministic logic
            extraction_result = await extract_claims(transcription)
            claims = extraction_result.get("claims", [transcription])
            
            # Single verdict logic (Point 6)
            results = await check_claims_batch(claims)
            if results:
                # Prioritize FALSE, then TRUE, then UNCERTAIN
                all_verdicts = [r.get("verdict", "UNCERTAIN").upper() for r in results]
                if "FALSE" in all_verdicts:
                    verdict = "FALSE"
                elif "TRUE" in all_verdicts:
                    # If no FALSE, but at least one TRUE
                    verdict = "TRUE"
                else:
                    verdict = "UNCERTAIN"
                
                # Get the first matching explanation
                explanation = next((r.get("reason") for r in results if r.get("verdict").upper() == verdict), "No explanation available.")
            else:
                verdict = "UNCERTAIN"
                explanation = "This claim cannot be verified with available information."

            # 6. Counter Message
            counter_message = generate_counter_message(transcription, verdict)
            
            # Store in Cache
            store_result(normalized, {
                "verdict": verdict,
                "explanation": explanation,
                "virality_score": virality_score,
                "counter_message": counter_message
            })

        # 7. Confidence Score (Point 9)
        confidence = calculate_confidence(verdict, transcription)

        # 8. Log to data.json (Point 13)
        log_pipeline_result({
            "text": transcription,
            "verdict": verdict,
            "virality_score": virality_score,
            "confidence": confidence['confidence_score'],
            "cached": cached
        })

        # 9. Format WhatsApp Message (Point 10 - EXACT)
        response_text = (
            f"📝 Transcription:\n{transcription}\n\n"
            f"⚠️ Verdict:\n{verdict}\n\n"
            f"📊 Virality Score:\n{virality_score}/10\n\n"
            f"📢 Counter Message:\n{counter_message or 'No corrective message needed.'}\n\n"
            f"🔍 Confidence:\n{confidence['confidence_level']} ({confidence['confidence_score']}%)"
        )

        # 10. Send Response (Point 11)
        if settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_phone_number:
            try:
                client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
                client.messages.create(
                    body=response_text,
                    from_=settings.twilio_phone_number,
                    to=sender
                )
                logger.info(f"Response sent to {sender}")
            except Exception as twilio_e:
                logger.error(f"Twilio error: {twilio_e}")
        else:
            logger.error("Twilio credentials missing. No response sent.")

    except Exception as e:
        logger.error(f"System failure: {e}")
        # Final fail-safe default message (Point 12)
        try:
             client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
             client.messages.create(
                body="⚠️ I encountered an error processing your message. Please try again later.",
                from_=settings.twilio_phone_number,
                to=sender
             )
        except:
             pass

@router.post("/")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    # Point 4: Use request.form() to get Twilio data
    form_data = await request.form()
    sender = form_data.get("From", "")
    body = form_data.get("Body", "")
    num_media = int(form_data.get("NumMedia", 0)) # Point 4
    media_url = form_data.get("MediaUrl0") if num_media > 0 else None
    
    background_tasks.add_task(process_whatsapp_message, sender, body, media_url)
    return Response(content="<Response></Response>", media_type="application/xml")
