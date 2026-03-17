import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.routes import whatsapp
from app.api import test_pipeline, audio

# Initialize logger for Point 3
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="FastAPI service for WhatsApp bot with Whisper transcription and Fact-Checking",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(whatsapp.router, prefix="/api/webhooks/whatsapp", tags=["Webhooks"])
app.include_router(test_pipeline.router, prefix="/test", tags=["Test"])
app.include_router(audio.router, prefix="/api/analysis", tags=["Analysis"])

# Point 3: Startup Validation (Log but do not crash)
@app.on_event("startup")
async def startup_event():
    logger.info(f"Welcome to {settings.app_name}")
    if not settings.twilio_account_sid or not settings.twilio_auth_token or not settings.twilio_phone_number:
        logger.error("CRITICAL ERROR: Twilio configuration missing (SID, TOKEN, or PHONE NUMBER).")
    else:
        logger.info("Twilio configuration validated. System ready in offline mode.")

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.app_name}", "environment": settings.environment}
