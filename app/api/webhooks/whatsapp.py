import os
import httpx
from fastapi import APIRouter, Request, BackgroundTasks, Form
from fastapi.responses import Response
from typing import Optional

from app.core.config import get_settings
from app.services.transcription import transcribe_audio
from app.services.extraction import extract_claims
from app.services.fact_check import check_claims_batch
from app.services.response import generate_response

router = APIRouter()
settings = get_settings()

async def download_media(media_url: str, auth_tuple: tuple) -> str:
    """
    Download media from Twilio to a local temporary file.
    """
    # Simple temporary file path in the current directory for cross-platform compatibility
    file_path = f"temp_{media_url.split('/')[-1]}.ogg"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(media_url, auth=auth_tuple)
        response.raise_for_status()
        with open(file_path, "wb") as f:
            f.write(response.content)
            
    return file_path

async def process_message(
    sender: str, 
    body: str, 
    media_url: Optional[str] = None, 
    media_type: Optional[str] = None
):
    """
    Background task to process the incoming message.
    """
    text_to_process = body

    try:
        if media_url and media_type and media_type.startswith("audio/"):
            # 1. Download audio and transcribe using Whisper
            print(f"Processing audio from {sender}")
            auth = (settings.twilio_account_sid, settings.twilio_auth_token)
            audio_path = await download_media(media_url, auth)
            
            text_to_process = await transcribe_audio(audio_path)
            print(f"Transcription: {text_to_process}")
            
            # Clean up temporary file
            if os.path.exists(audio_path):
                os.remove(audio_path)
                
        # 2. Extract Claims
        print(f"Extracting claims from: {text_to_process}")
        extraction_result = await extract_claims(text_to_process)
        claims = extraction_result.get("claims", [])
        
        # 3. Fact Check
        print(f"Fact-checking {len(claims)} claims")
        results = await check_claims_batch(claims)
        
        # 4. Generate Response
        print("Generating response")
        final_response = await generate_response(text_to_process, claims, results)
        
        # 5. Send reply via Twilio WhatsApp API
        print(f"Final response to {sender}: {final_response}")
        
        if settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_phone_number:
            from twilio.rest import Client
            twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
            
            # Since twilio sync client is blocking, we can run it in a thread or just call it directly
            # For a pure async app, we could use httpx to call Twilio API directly, but the SDK is standard
            # We'll use the SDK
            message = twilio_client.messages.create(
                body=final_response,
                from_=settings.twilio_phone_number,
                to=sender
            )
            print(f"Message sent successfully. SID: {message.sid}")
        else:
            print("Warning: Twilio credentials not fully configured. Cannot send reply message.")
        
    except Exception as e:
        print(f"Error processing message from {sender}: {e}")

@router.post("/")
async def whatsapp_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    Body: str = Form(""),
    From: str = Form(""),
    NumMedia: int = Form(0),
):
    """
    Webhook endpoint to receive messages from Twilio WhatsApp API.
    """
    form_data = await request.form()
    
    media_url = form_data.get("MediaUrl0") if NumMedia > 0 else None
    media_type = form_data.get("MediaContentType0") if NumMedia > 0 else None
    
    print(f"Received message from {From}: {Body}")
    if media_url:
        print(f"Media details: {media_url} ({media_type})")
        
    # Process the message asynchronously to return a quick 200 OK to Twilio
    background_tasks.add_task(process_message, From, Body, media_url, media_type)
    
    # Twilio expects a TwiML response or a simple 200 OK
    return Response(content="<Response></Response>", media_type="application/xml")
