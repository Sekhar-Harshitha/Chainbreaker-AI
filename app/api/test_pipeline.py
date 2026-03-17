from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import logging
import json
import datetime
from pathlib import Path

from app.core.config import get_settings
from app.services.extraction import extract_claims
from app.services.fact_check import check_claims_batch
from app.services.response import generate_response
from app.services.virality import calculate_virality_score
from app.services.cache import normalize_text, get_cached_result, store_result
from app.services.counter_message import generate_counter_message
from app.services.confidence import calculate_confidence

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)

DATA_LOG_FILE = Path("data.json")

def log_pipeline_result(result: dict):
    """
    Log result to a json file for the dashboard.
    """
    try:
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            **result
        }
        with open(DATA_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        logger.error(f"Error logging result: {e}")

class TestInput(BaseModel):
    text: str

class PipelineTestResponse(BaseModel):
    transcription: str
    claims: List[str]
    verdict: str
    explanation: str
    virality_score: int
    virality_reasons: List[str]
    cached: bool
    counter_message: Optional[str] = None
    confidence_score: int
    confidence_level: str
    source_count: int

@router.post("/", response_model=PipelineTestResponse)
async def test_pipeline(input: TestInput):
    """
    Test the fact-checking pipeline inside an endpoint.
    """
    transcription = input.text
    print(f"Transcription: {transcription}")

    # Step 1b: Calculate virality risk score (always fast, rule-based)
    virality_result = calculate_virality_score(transcription)
    virality_score = virality_result["score"]
    virality_reasons = virality_result["reasons"]
    print(f"Virality Score: {virality_score}")
    print(f"Virality Reasons: {virality_reasons}")

    # Check cache before running expensive pipeline steps
    normalized = normalize_text(transcription)
    cached_result = get_cached_result(normalized)
    if cached_result:
        confidence = calculate_confidence(cached_result.get("verdict", "UNCERTAIN"), transcription)
        log_pipeline_result({
            "text": transcription,
            "verdict": cached_result.get("verdict"),
            "virality_score": cached_result.get("virality_score"),
            "cached": True,
            **confidence
        })
        return PipelineTestResponse(
            transcription=transcription,
            cached=True,
            **cached_result,
            **confidence
        )

    if not settings.openai_api_key:
        # Basic keyword-based fact-check logic (no API key required)
        FALSE_KEYWORDS = {"cure", "miracle", "guarantee"}
        contains_false_keyword = any(kw in transcription.lower() for kw in FALSE_KEYWORDS)

        if contains_false_keyword:
            verdict = "FALSE"
            explanation = "This claim is not supported by scientific evidence."
        else:
            verdict = "UNCERTAIN"
            explanation = "Insufficient evidence to verify this claim."

        claims = [transcription]

        print(f"Claims: {claims}")
        print(f"Verdict: {verdict}")

        counter_message = generate_counter_message(transcription, verdict)

        result_to_cache = {
            "claims": claims,
            "verdict": verdict,
            "explanation": explanation,
            "virality_score": virality_score,
            "virality_reasons": virality_reasons,
            "counter_message": counter_message,
        }
        store_result(normalized, result_to_cache)

        confidence = calculate_confidence(verdict, transcription)
        
        response = PipelineTestResponse(
            transcription=transcription,
            cached=False,
            confidence_score=confidence["confidence_score"],
            confidence_level=confidence["confidence_level"],
            source_count=confidence["source_count"],
            **result_to_cache
        )
        
        log_pipeline_result({
            "text": transcription,
            "verdict": verdict,
            "virality_score": virality_score,
            "cached": False,
            **confidence
        })
        
        return response


    # 1. Extraction step
    extraction_result = await extract_claims(transcription)
    claims = extraction_result.get("claims", [])
    print(f"Claims: {claims}")
    
    # 2. Fact Check step
    results = await check_claims_batch(claims)
    
    # Simple overall verdict logic
    verdict = "UNCERTAIN"
    if results:
        all_verdicts = [r.get("verdict", "").upper() for r in results]
        if "FALSE" in all_verdicts:
            verdict = "FALSE"
        elif all(v == "TRUE" for v in all_verdicts):
            verdict = "TRUE"
        elif "MIXED" in all_verdicts:
            verdict = "MIXED"
    
    print(f"Verdict: {verdict}")
    
    # 3. Response Generation Step
    explanation = await generate_response(transcription, claims, results)

    counter_message = generate_counter_message(transcription, verdict)

    result_to_cache = {
        "claims": claims,
        "verdict": verdict,
        "explanation": explanation,
        "virality_score": virality_score,
        "virality_reasons": virality_reasons,
        "counter_message": counter_message,
    }
    store_result(normalized, result_to_cache)

    confidence = calculate_confidence(verdict, transcription)

    log_pipeline_result({
        "text": transcription,
        "verdict": verdict,
        "virality_score": virality_score,
        "cached": False,
        **confidence
    })

    return PipelineTestResponse(
        transcription=transcription,
        cached=False,
        **result_to_cache,
        **confidence
    )
