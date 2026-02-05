# Voice Deepfake Detection API

A REST API system that detects whether a voice sample is AI-generated or spoken by a real human. Supports Tamil, English, Hindi, Malayalam, and Telugu languages.

## 🎯 Features

- **Multi-language Support**: Tamil, English, Hindi, Malayalam, Telugu
- **Base64 Audio Processing**: Accepts MP3 files encoded in base64
- **Confidence Scoring**: Returns confidence scores between 0.0 and 1.0
- **REST API**: Simple, secure API with API key authentication
- **Advanced Detection**: Uses multiple audio analysis techniques including:
  - Spectral analysis
  - MFCC (Mel-frequency cepstral coefficients)
  - Pitch and formant analysis
  - Energy distribution patterns
  - Phase consistency checks
  - Artifact detection

## 📋 API Specification

### Endpoint
```
POST /api/v1/analyze
```

### Request Format

**Headers:**
```
X-API-Key: your-secure-api-key-here
Content-Type: application/json
```

**Body:**
```json
{
  "audio_base64": "base64_encoded_mp3_string",
  "language": "english"
}
```

**Supported Languages:**
- `tamil`
- `english`
- `hindi`
- `malayalam`
- `telugu`

### Response Format

```json
{
  "classification": "AI_GENERATED",
  "confidence_score": 0.8542,
  "language": "english",
  "timestamp": "2024-02-05T10:30:45.123456",
  "processing_time_ms": 234.56
}
```

**Fields:**
- `classification`: Either `"AI_GENERATED"` or `"HUMAN"`
- `confidence_score`: Float between 0.0 and 1.0
- `language`: The language of the audio sample
- `timestamp`: ISO 8601 timestamp of analysis
- `processing_time_ms`: Processing time in milliseconds

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check if running
curl http://localhost:8000/api/v1/health
```

### Option 2: Local Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

The API will be available at `http://localhost:8000`

## 📝 Usage Examples

### Python Client

```python
import requests
import base64

# Configuration
API_URL = "http://localhost:8000/api/v1/analyze"
API_KEY = "your-secure-api-key-here"

# Encode audio file
with open("sample.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode('utf-8')

# Make request
response = requests.post(
    API_URL,
    headers={"X-API-Key": API_KEY},
    json={
        "audio_base64": audio_base64,
        "language": "english"
    }
)

result = response.json()
print(f"Classification: {result['classification']}")
print(f"Confidence: {result['confidence_score']:.2%}")
```

### cURL

```bash
# Encode audio to base64
AUDIO_BASE64=$(base64 -w 0 sample.mp3)

# Make API request
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "X-API-Key: your-secure-api-key-here" \
  -H "Content-Type: application/json" \
  -d "{
    \"audio_base64\": \"$AUDIO_BASE64\",
    \"language\": \"english\"
  }"
```

### JavaScript/Node.js

```javascript
const fs = require('fs');
const axios = require('axios');

// Read and encode audio file
const audioBuffer = fs.readFileSync('sample.mp3');
const audioBase64 = audioBuffer.toString('base64');

// Make API request
axios.post('http://localhost:8000/api/v1/analyze', {
  audio_base64: audioBase64,
  language: 'english'
}, {
  headers: {
    'X-API-Key': 'your-secure-api-key-here',
    'Content-Type': 'application/json'
  }
})
.then(response => {
  console.log('Classification:', response.data.classification);
  console.log('Confidence:', response.data.confidence_score);
})
.catch(error => {
  console.error('Error:', error.response?.data || error.message);
});
```

## 🔐 Security

### API Key Configuration

Change the default API key in `main.py`:

```python
API_KEY = "your-secure-api-key-here"  # Change this!
```

Or set it as an environment variable:

```bash
export API_KEY="your-secure-api-key-here"
python main.py
```

### Production Deployment Recommendations

1. **Use HTTPS**: Deploy behind a reverse proxy (nginx/Apache) with SSL
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Strong API Keys**: Use cryptographically secure random keys
4. **Logging**: Monitor API usage and suspicious activity
5. **Input Validation**: Already implemented in the API
6. **CORS**: Configure CORS policies based on your needs

## 🧪 Testing

Run the test client:

```bash
python test_client.py
```

This will:
1. Check API health
2. Display API information
3. Show example usage

To test with an actual audio file:

```python
from test_client import analyze_voice

analyze_voice("path/to/audio.mp3", "english")
```

## 📊 Detection Methodology

The system uses multiple analysis techniques to detect AI-generated voices:

### 1. Spectral Analysis
- Analyzes frequency distribution patterns
- AI voices often have more uniform spectral characteristics

### 2. MFCC Analysis
- Mel-frequency cepstral coefficients
- Critical for voice texture analysis
- AI lacks natural micro-variations

### 3. Temporal Features
- Zero-crossing rate
- Energy distribution over time
- AI voices show unnatural consistency

### 4. Pitch Analysis
- Fundamental frequency tracking
- AI often lacks natural pitch jitter
- Formant transition patterns

### 5. Artifact Detection
- Phase consistency checks
- High-frequency artifacts
- Periodic pattern detection
- Micro-jitter analysis

## 📈 Performance

- **Processing Time**: Typically 100-500ms per audio sample
- **Accuracy**: Depends on audio quality and length
- **Recommended Audio**: 
  - Duration: 3-10 seconds
  - Format: MP3
  - Sample Rate: 16kHz or higher
  - Bitrate: 128kbps or higher

## 🛠️ API Endpoints

### Analyze Voice
```
POST /api/v1/analyze
```
Main endpoint for voice analysis

### Health Check
```
GET /api/v1/health
```
Returns API health status and supported languages

### API Information
```
GET /api/v1/info
```
Returns comprehensive API information

## 🔧 Configuration

### Environment Variables

```bash
# API Configuration
API_KEY=your-secure-api-key-here
PORT=8000
HOST=0.0.0.0

# Logging
LOG_LEVEL=INFO
```

## 📦 Dependencies

- **FastAPI**: Web framework
- **librosa**: Audio analysis
- **numpy**: Numerical operations
- **uvicorn**: ASGI server
- **pydantic**: Data validation

See `requirements.txt` for complete list.

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid API Key"**
   - Ensure the `X-API-Key` header matches the server configuration

2. **"Invalid base64 encoding"**
   - Verify the audio file is properly encoded
   - Check for whitespace or newlines in base64 string

3. **"Error processing audio"**
   - Ensure the file is a valid MP3
   - Check audio file isn't corrupted
   - Verify file size is reasonable (< 10MB)

4. **Connection refused**
   - Ensure the server is running
   - Check the port isn't blocked by firewall
   - Verify correct URL and port

## 📄 License

This is a demonstration project for a hackathon/competition.

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Test with the provided sample client

## 🚢 Deployment

### Cloud Platforms

#### Heroku
```bash
heroku create your-app-name
heroku container:push web
heroku container:release web
```

#### AWS EC2
```bash
# Install Docker
# Clone repository
docker-compose up -d
```

#### Google Cloud Run
```bash
gcloud run deploy voice-deepfake-api \
  --source . \
  --platform managed \
  --region us-central1
```

### Monitoring

Add application monitoring:
- Health check endpoint: `/api/v1/health`
- Metrics: Response time, error rates
- Logging: All requests and errors logged

## 📊 Example Response Interpretation

```json
{
  "classification": "AI_GENERATED",
  "confidence_score": 0.8542
}
```

- **Confidence > 0.8**: High confidence in classification
- **Confidence 0.6-0.8**: Moderate confidence
- **Confidence < 0.6**: Low confidence, may need review

## 🎓 Technical Details

### Audio Processing Pipeline

1. **Base64 Decoding**: Convert input to audio bytes
2. **Audio Loading**: Load with librosa (automatic resampling)
3. **Feature Extraction**: Extract 50+ audio features
4. **Analysis**: Apply multiple detection algorithms
5. **Classification**: Determine if AI or Human
6. **Confidence Calculation**: Calculate reliability score

### Key Indicators of AI-Generated Voice

- Unnaturally consistent energy levels
- Reduced spectral variation
- Lack of micro-pitch variations (jitter)
- Periodic artifacts in frequency domain
- Smooth formant transitions
- Consistent phase relationships

## 🔄 API Versioning

Current version: `v1`

Endpoints are versioned: `/api/v1/analyze`

Future versions will maintain backward compatibility.
