"""
Voice Deepfake Detection API
Detects AI-generated vs Human voice samples in Tamil, English, Hindi, Malayalam, Telugu
"""

from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, validator
import base64
import io
import librosa
import numpy as np
from typing import Literal
import uvicorn
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Voice Deepfake Detection API",
    description="API for detecting AI-generated vs Human voice samples",
    version="1.0.0"
)

# API Key configuration
import os
API_KEY = os.getenv("API_KEY", "168ef25828540dda5abd5f957c32dc3d")  # Reads from environment variable
api_key_header = APIKeyHeader(name="X-API-Key")

# Supported languages
SUPPORTED_LANGUAGES = ["tamil", "english", "hindi", "malayalam", "telugu"]

# Request/Response Models
class VoiceAnalysisRequest(BaseModel):
    audio_base64: str = Field(..., description="Base64-encoded MP3 audio file")
    language: Literal["tamil", "english", "hindi", "malayalam", "telugu"] = Field(
        ..., description="Language of the audio sample"
    )
    
    @validator('audio_base64')
    def validate_base64(cls, v):
        try:
            base64.b64decode(v)
            return v
        except Exception:
            raise ValueError("Invalid base64 encoding")

class VoiceAnalysisResponse(BaseModel):
    classification: Literal["AI_GENERATED", "HUMAN"]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    language: str
    timestamp: str
    processing_time_ms: float

# API Key validation
async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

# Feature extraction functions
def extract_audio_features(audio_data: np.ndarray, sr: int) -> dict:
    """
    Extract comprehensive audio features for deepfake detection
    """
    features = {}
    
    # 1. Spectral features
    spectral_centroid = librosa.feature.spectral_centroid(y=audio_data, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio_data, sr=sr)
    
    features['spectral_centroid_mean'] = np.mean(spectral_centroid)
    features['spectral_centroid_std'] = np.std(spectral_centroid)
    features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
    features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
    
    # 2. MFCC features (key for voice analysis)
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=20)
    features['mfcc_mean'] = np.mean(mfccs, axis=1)
    features['mfcc_std'] = np.std(mfccs, axis=1)
    
    # 3. Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(audio_data)
    features['zcr_mean'] = np.mean(zcr)
    features['zcr_std'] = np.std(zcr)
    
    # 4. Chroma features
    chroma = librosa.feature.chroma_stft(y=audio_data, sr=sr)
    features['chroma_mean'] = np.mean(chroma)
    features['chroma_std'] = np.std(chroma)
    
    # 5. RMS Energy
    rms = librosa.feature.rms(y=audio_data)
    features['rms_mean'] = np.mean(rms)
    features['rms_std'] = np.std(rms)
    
    # 6. Pitch and formants
    pitches, magnitudes = librosa.piptrack(y=audio_data, sr=sr)
    features['pitch_mean'] = np.mean(pitches[pitches > 0]) if np.any(pitches > 0) else 0
    
    return features

def detect_deepfake_indicators(features: dict, language: str) -> tuple[str, float]:
    """
    Analyze features to detect AI-generated voice
    
    AI-generated voices often have:
    - More uniform spectral characteristics
    - Reduced micro-variations in pitch
    - Artifacts in high-frequency ranges
    - Unnatural formant transitions
    - Consistent energy levels (less natural variation)
    """
    
    ai_score = 0.0
    indicators = 0
    
    # 1. Check spectral consistency (AI voices tend to be more consistent)
    spectral_variation = features['spectral_centroid_std'] / (features['spectral_centroid_mean'] + 1e-6)
    if spectral_variation < 0.15:  # Low variation suggests AI
        ai_score += 0.2
        indicators += 1
    
    # 2. MFCC analysis (AI often has less variation)
    mfcc_variation = np.mean(features['mfcc_std']) / (np.mean(np.abs(features['mfcc_mean'])) + 1e-6)
    if mfcc_variation < 0.3:
        ai_score += 0.25
        indicators += 1
    
    # 3. Zero crossing rate consistency
    zcr_consistency = features['zcr_std'] / (features['zcr_mean'] + 1e-6)
    if zcr_consistency < 0.2:
        ai_score += 0.15
        indicators += 1
    
    # 4. Energy uniformity (AI tends to have more uniform energy)
    energy_variation = features['rms_std'] / (features['rms_mean'] + 1e-6)
    if energy_variation < 0.25:
        ai_score += 0.2
        indicators += 1
    
    # 5. Chroma consistency
    chroma_consistency = features['chroma_std'] / (features['chroma_mean'] + 1e-6)
    if chroma_consistency < 0.3:
        ai_score += 0.2
        indicators += 1
    
    # Normalize score
    if indicators > 0:
        confidence = min(ai_score, 1.0)
    else:
        confidence = 0.3  # Default low confidence if no clear indicators
    
    # Determine classification
    threshold = 0.5
    if confidence >= threshold:
        classification = "AI_GENERATED"
    else:
        classification = "HUMAN"
        confidence = 1.0 - confidence  # Invert confidence for HUMAN classification
    
    return classification, round(confidence, 4)

@app.post("/api/v1/analyze", response_model=VoiceAnalysisResponse)
async def analyze_voice(
    request: VoiceAnalysisRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Analyze voice sample to detect if it's AI-generated or human
    """
    start_time = datetime.now()
    
    try:
        # Decode base64 audio
        audio_bytes = base64.b64decode(request.audio_base64)
        
        # Load audio using librosa
        audio_data, sample_rate = librosa.load(
            io.BytesIO(audio_bytes),
            sr=None,  # Preserve original sample rate
            mono=True
        )
        
        # Extract features
        features = extract_audio_features(audio_data, sample_rate)
        
        # Detect deepfake
        classification, confidence = detect_deepfake_indicators(features, request.language)
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        logger.info(f"Analyzed {request.language} audio: {classification} ({confidence})")
        
        return VoiceAnalysisResponse(
            classification=classification,
            confidence_score=confidence,
            language=request.language,
            timestamp=datetime.utcnow().isoformat(),
            processing_time_ms=round(processing_time, 2)
        )
        
    except Exception as e:
        logger.error(f"Error analyzing voice: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint - API welcome"""
    return {
        "message": "Voice Deepfake Detection API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "health": "/api/v1/health",
            "info": "/api/v1/info",
            "analyze": "POST /api/v1/analyze",
            "docs": "/docs"
        },
        "supported_languages": SUPPORTED_LANGUAGES
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "supported_languages": SUPPORTED_LANGUAGES,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Voice Deepfake Detection API",
        "version": "1.0.0",
        "supported_languages": SUPPORTED_LANGUAGES,
        "supported_formats": ["MP3"],
        "input_encoding": "base64",
        "classification_types": ["AI_GENERATED", "HUMAN"],
        "confidence_range": [0.0, 1.0]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
