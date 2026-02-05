"""
Test client for Voice Deepfake Detection API
"""

import requests
import base64
import json
from pathlib import Path

# API Configuration
API_URL = "http://localhost:8000/api/v1/analyze"
API_KEY = "your-secure-api-key-here"  # Must match the server API key

def encode_audio_to_base64(audio_file_path: str) -> str:
    """Convert audio file to base64 string"""
    with open(audio_file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        base64_string = base64.b64encode(audio_bytes).decode('utf-8')
    return base64_string

def analyze_voice(audio_file_path: str, language: str):
    """
    Send audio file to API for analysis
    
    Args:
        audio_file_path: Path to MP3 audio file
        language: One of ['tamil', 'english', 'hindi', 'malayalam', 'telugu']
    """
    
    print(f"Analyzing audio file: {audio_file_path}")
    print(f"Language: {language}")
    print("-" * 60)
    
    # Encode audio to base64
    try:
        audio_base64 = encode_audio_to_base64(audio_file_path)
        print(f"✓ Audio file encoded (size: {len(audio_base64)} chars)")
    except FileNotFoundError:
        print(f"✗ Error: File not found: {audio_file_path}")
        return
    except Exception as e:
        print(f"✗ Error encoding file: {e}")
        return
    
    # Prepare request
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "audio_base64": audio_base64,
        "language": language
    }
    
    # Send request
    try:
        print("Sending request to API...")
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            print("\n" + "=" * 60)
            print("ANALYSIS RESULTS")
            print("=" * 60)
            print(f"Classification: {result['classification']}")
            print(f"Confidence Score: {result['confidence_score']:.4f}")
            print(f"Language: {result['language']}")
            print(f"Timestamp: {result['timestamp']}")
            print(f"Processing Time: {result['processing_time_ms']:.2f} ms")
            print("=" * 60)
            
            # Interpretation
            if result['classification'] == 'AI_GENERATED':
                print(f"\n⚠️  This voice sample is likely AI-GENERATED")
                print(f"   Confidence: {result['confidence_score']*100:.1f}%")
            else:
                print(f"\n✓  This voice sample is likely HUMAN")
                print(f"   Confidence: {result['confidence_score']*100:.1f}%")
                
        elif response.status_code == 403:
            print("\n✗ Authentication failed. Check your API key.")
        else:
            print(f"\n✗ Error: {response.status_code}")
            print(f"   Message: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Could not connect to API server.")
        print("   Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"\n✗ Error: {e}")

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get("http://localhost:8000/api/v1/health")
        if response.status_code == 200:
            print("✓ API is healthy")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print("✗ API health check failed")
            return False
    except:
        print("✗ Cannot connect to API")
        return False

def get_api_info():
    """Get API information"""
    try:
        response = requests.get("http://localhost:8000/api/v1/info")
        if response.status_code == 200:
            print("\nAPI Information:")
            print(json.dumps(response.json(), indent=2))
    except:
        print("✗ Cannot get API info")

# Example usage
if __name__ == "__main__":
    print("Voice Deepfake Detection API - Test Client")
    print("=" * 60)
    
    # Check API health
    print("\nChecking API health...")
    if not check_api_health():
        print("\nPlease start the API server first:")
        print("  python main.py")
        exit(1)
    
    # Get API info
    get_api_info()
    
    print("\n" + "=" * 60)
    print("EXAMPLE USAGE")
    print("=" * 60)
    
    # Example: Analyze a sample audio file
    # Replace with your actual audio file path
    sample_audio = "sample_audio.mp3"
    
    print(f"\nTo analyze an audio file, use:")
    print(f'  analyze_voice("{sample_audio}", "english")')
    print(f"\nSupported languages: tamil, english, hindi, malayalam, telugu")
    
    # Uncomment below to test with an actual file
    # analyze_voice("path/to/your/audio.mp3", "english")
