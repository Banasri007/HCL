# API Response Examples

## Success Responses

### AI-Generated Voice Detection

**Request:**
```json
{
  "audio_base64": "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4Ljc2LjEwMAAAAAAAAAAAAAAA...",
  "language": "english"
}
```

**Response (AI Detected - High Confidence):**
```json
{
  "classification": "AI_GENERATED",
  "confidence_score": 0.8765,
  "language": "english",
  "timestamp": "2024-02-05T14:32:10.123456",
  "processing_time_ms": 234.56
}
```

**Response (AI Detected - Moderate Confidence):**
```json
{
  "classification": "AI_GENERATED",
  "confidence_score": 0.6543,
  "language": "tamil",
  "timestamp": "2024-02-05T14:35:22.789012",
  "processing_time_ms": 198.34
}
```

### Human Voice Detection

**Response (Human - High Confidence):**
```json
{
  "classification": "HUMAN",
  "confidence_score": 0.9234,
  "language": "hindi",
  "timestamp": "2024-02-05T14:40:15.345678",
  "processing_time_ms": 267.89
}
```

**Response (Human - Moderate Confidence):**
```json
{
  "classification": "HUMAN",
  "confidence_score": 0.7123,
  "language": "malayalam",
  "timestamp": "2024-02-05T14:45:30.901234",
  "processing_time_ms": 223.45
}
```

## Error Responses

### Invalid API Key
**Status Code:** 403 Forbidden

```json
{
  "detail": "Invalid API Key"
}
```

### Invalid Language
**Status Code:** 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": ["body", "language"],
      "msg": "unexpected value; permitted: 'tamil', 'english', 'hindi', 'malayalam', 'telugu'",
      "type": "value_error.const"
    }
  ]
}
```

### Invalid Base64 Encoding
**Status Code:** 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": ["body", "audio_base64"],
      "msg": "Invalid base64 encoding",
      "type": "value_error"
    }
  ]
}
```

### Processing Error
**Status Code:** 500 Internal Server Error

```json
{
  "detail": "Error processing audio: Unable to decode audio file"
}
```

## Health Check Response

**Endpoint:** GET /api/v1/health

**Response:**
```json
{
  "status": "healthy",
  "supported_languages": [
    "tamil",
    "english",
    "hindi",
    "malayalam",
    "telugu"
  ],
  "timestamp": "2024-02-05T14:50:00.000000"
}
```

## API Info Response

**Endpoint:** GET /api/v1/info

**Response:**
```json
{
  "name": "Voice Deepfake Detection API",
  "version": "1.0.0",
  "supported_languages": [
    "tamil",
    "english",
    "hindi",
    "malayalam",
    "telugu"
  ],
  "supported_formats": ["MP3"],
  "input_encoding": "base64",
  "classification_types": ["AI_GENERATED", "HUMAN"],
  "confidence_range": [0.0, 1.0]
}
```

## Multi-Language Examples

### Tamil
```json
{
  "classification": "HUMAN",
  "confidence_score": 0.8456,
  "language": "tamil",
  "timestamp": "2024-02-05T15:00:00.000000",
  "processing_time_ms": 245.67
}
```

### Hindi
```json
{
  "classification": "AI_GENERATED",
  "confidence_score": 0.7890,
  "language": "hindi",
  "timestamp": "2024-02-05T15:05:00.000000",
  "processing_time_ms": 212.34
}
```

### Malayalam
```json
{
  "classification": "HUMAN",
  "confidence_score": 0.9012,
  "language": "malayalam",
  "timestamp": "2024-02-05T15:10:00.000000",
  "processing_time_ms": 198.56
}
```

### Telugu
```json
{
  "classification": "AI_GENERATED",
  "confidence_score": 0.8234,
  "language": "telugu",
  "timestamp": "2024-02-05T15:15:00.000000",
  "processing_time_ms": 234.89
}
```

## Confidence Score Interpretation

| Range | Interpretation | Recommendation |
|-------|---------------|----------------|
| 0.9 - 1.0 | Very High Confidence | High reliability |
| 0.8 - 0.9 | High Confidence | Reliable result |
| 0.7 - 0.8 | Good Confidence | Generally reliable |
| 0.6 - 0.7 | Moderate Confidence | Review recommended |
| 0.5 - 0.6 | Low Confidence | Manual review needed |
| < 0.5 | Very Low Confidence | Uncertain, needs verification |

## Processing Time Benchmarks

| Audio Duration | Typical Processing Time |
|----------------|------------------------|
| 1-3 seconds    | 150-250 ms            |
| 3-5 seconds    | 250-400 ms            |
| 5-10 seconds   | 400-700 ms            |
| 10+ seconds    | 700+ ms               |

Note: Processing times may vary based on:
- Server load
- Audio quality and sample rate
- Complexity of audio content
- Network latency
