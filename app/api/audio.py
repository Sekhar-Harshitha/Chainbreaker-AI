from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import os
import uuid
import logging
from app.services.transcription import transcribe_audio
from app.services.extraction import extract_claims
from app.services.fact_check import check_claims_batch
from app.services.virality import calculate_virality_score
from app.services.confidence import calculate_confidence
from app.services.counter_message import generate_counter_message

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/analyze")
async def analyze_audio(file: UploadFile = File(...)):
    """
    Upload an audio file, transcribe it, and run the fact-check pipeline.
    """
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    temp_file_path = UPLOAD_DIR / f"{file_id}{file_extension}"

    try:
        # Save uploaded file
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 1. Transcribe
        transcription = await transcribe_audio(str(temp_file_path))
        
        # 2. Extract Claims
        extraction_result = await extract_claims(transcription)
        claims = extraction_result.get("claims", [transcription])

        # 3. Fact Check
        results = await check_claims_batch(claims)
        
        # Determine overall verdict
        verdict = "UNCERTAIN"
        explanation = "This claim cannot be verified with available information."
        if results:
            all_verdicts = [r.get("verdict", "UNCERTAIN").upper() for r in results]
            if "FALSE" in all_verdicts:
                verdict = "FALSE"
            elif "TRUE" in all_verdicts:
                verdict = "TRUE"
            
            # Get explanation for the verdict
            matching_result = next((r for r in results if r.get("verdict").upper() == verdict), None)
            if matching_result:
                explanation = matching_result.get("reason", matching_result.get("explanation", explanation))

        # 4. Virality Score
        virality_result = calculate_virality_score(transcription)
        
        # 5. Counter Message
        counter_message = generate_counter_message(transcription, verdict)

        # 6. Confidence Score
        confidence = calculate_confidence(verdict, transcription)

        return {
            "file_id": file_id,
            "transcription": transcription,
            "verdict": verdict,
            "explanation": explanation,
            "virality_score": virality_result["score"],
            "virality_reasons": virality_result["reasons"],
            "counter_message": counter_message,
            "confidence_score": confidence["confidence_score"],
            "confidence_level": confidence["confidence_level"],
            "source_count": confidence["source_count"],
            "claims": claims
        }

    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temp file
        if temp_file_path.exists():
            os.remove(temp_file_path)

@router.post("/analyze-text")
async def analyze_text(data: dict):
    """
    Analyze text directly for fact-checking.
    """
    text = data.get("text", "")
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    try:
        # 1. Extract Claims
        extraction_result = await extract_claims(text)
        claims = extraction_result.get("claims", [text])

        # 2. Fact Check
        results = await check_claims_batch(claims)
        
        # Determine overall verdict
        verdict = "UNCERTAIN"
        explanation = "This claim cannot be verified with available information."
        if results:
            all_verdicts = [r.get("verdict", "UNCERTAIN").upper() for r in results]
            if "FALSE" in all_verdicts:
                verdict = "FALSE"
            elif "TRUE" in all_verdicts:
                verdict = "TRUE"
            
            matching_result = next((r for r in results if r.get("verdict").upper() == verdict), None)
            if matching_result:
                explanation = matching_result.get("reason", matching_result.get("explanation", explanation))

        # 3. Virality Score
        virality_result = calculate_virality_score(text)
        
        # 4. Counter Message
        counter_message = generate_counter_message(text, verdict)

        # 5. Confidence Score
        confidence = calculate_confidence(verdict, text)

        return {
            "transcription": text,
            "verdict": verdict,
            "explanation": explanation,
            "virality_score": virality_result["score"],
            "virality_reasons": virality_result["reasons"],
            "counter_message": counter_message,
            "confidence_score": confidence["confidence_score"],
            "confidence_level": confidence["confidence_level"],
            "source_count": confidence["source_count"],
            "claims": claims
        }
    except Exception as e:
        logger.error(f"Text analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
