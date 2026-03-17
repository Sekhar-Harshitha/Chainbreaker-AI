from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from dotenv import load_dotenv
import os

# Point 3 & 6: Ensure .env is loaded (Point 5 too)
load_dotenv()

class Settings(BaseSettings):
    app_name: str = "Chainbreaker Whisper Bot"
    environment: str = "development"
    debug: bool = True
    
    # Twilio API Keys (Point 5)
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

@lru_cache()
def get_settings():
    return Settings()
