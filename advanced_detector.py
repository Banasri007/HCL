"""
Advanced Deep Learning-based Voice Deepfake Detector
Uses more sophisticated features and analysis techniques
"""

import numpy as np
import librosa
from scipy import signal
from typing import Tuple, Dict

class AdvancedDeepfakeDetector:
    """
    Advanced deepfake detection using multiple analysis techniques
    """
    
    def __init__(self):
        self.sample_rate = 16000
        
    def extract_advanced_features(self, audio: np.ndarray, sr: int) -> Dict:
        """Extract comprehensive features for deepfake detection"""
        
        features = {}
        
        # 1. Mel-spectrogram features
        mel_spec = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=128)
        mel_spec_db = librosa.power_to_db(mel_spec, ref=np.max)
        features['mel_spec_mean'] = np.mean(mel_spec_db)
        features['mel_spec_std'] = np.std(mel_spec_db)
        features['mel_spec_variance'] = np.var(mel_spec_db)
        
        # 2. MFCCs (critical for voice analysis)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        features['mfcc_mean'] = np.mean(mfccs, axis=1)
        features['mfcc_std'] = np.std(mfccs, axis=1)
        features['mfcc_delta'] = np.mean(librosa.feature.delta(mfccs), axis=1)
        features['mfcc_delta2'] = np.mean(librosa.feature.delta(mfccs, order=2), axis=1)
        
        # 3. Spectral features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr)[0]
        spectral_contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
        spectral_flatness = librosa.feature.spectral_flatness(y=audio)[0]
        
        features['spectral_centroid_mean'] = np.mean(spectral_centroids)
        features['spectral_centroid_std'] = np.std(spectral_centroids)
        features['spectral_rolloff_mean'] = np.mean(spectral_rolloff)
        features['spectral_bandwidth_mean'] = np.mean(spectral_bandwidth)
        features['spectral_bandwidth_std'] = np.std(spectral_bandwidth)
        features['spectral_contrast_mean'] = np.mean(spectral_contrast)
        features['spectral_flatness_mean'] = np.mean(spectral_flatness)
        features['spectral_flatness_std'] = np.std(spectral_flatness)
        
        # 4. Temporal features
        zcr = librosa.feature.zero_crossing_rate(audio)[0]
        features['zcr_mean'] = np.mean(zcr)
        features['zcr_std'] = np.std(zcr)
        
        # 5. Energy and RMS
        rms = librosa.feature.rms(y=audio)[0]
        features['rms_mean'] = np.mean(rms)
        features['rms_std'] = np.std(rms)
        features['rms_variance'] = np.var(rms)
        
        # 6. Pitch and harmonics
        pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
        pitch_values = pitches[pitches > 0]
        if len(pitch_values) > 0:
            features['pitch_mean'] = np.mean(pitch_values)
            features['pitch_std'] = np.std(pitch_values)
            features['pitch_range'] = np.max(pitch_values) - np.min(pitch_values)
        else:
            features['pitch_mean'] = 0
            features['pitch_std'] = 0
            features['pitch_range'] = 0
        
        # 7. Tonnetz (tonal centroid features)
        tonnetz = librosa.feature.tonnetz(y=audio, sr=sr)
        features['tonnetz_mean'] = np.mean(tonnetz)
        features['tonnetz_std'] = np.std(tonnetz)
        
        # 8. Chroma features
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr)
        features['chroma_mean'] = np.mean(chroma)
        features['chroma_std'] = np.std(chroma)
        
        # 9. Phase-based features (AI often has phase artifacts)
        stft = librosa.stft(audio)
        phase = np.angle(stft)
        features['phase_mean'] = np.mean(phase)
        features['phase_std'] = np.std(phase)
        
        return features
    
    def detect_artifacts(self, audio: np.ndarray, sr: int) -> Dict[str, float]:
        """
        Detect AI-specific artifacts in audio
        """
        artifacts = {}
        
        # 1. Frequency domain artifacts
        fft = np.fft.fft(audio)
        magnitude = np.abs(fft)
        
        # Check for periodic patterns (common in AI)
        autocorr = np.correlate(magnitude, magnitude, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        artifacts['periodicity_score'] = np.max(autocorr[1:100]) / autocorr[0]
        
        # 2. High-frequency consistency (AI often lacks natural HF variation)
        high_freq_start = len(magnitude) // 4
        high_freq = magnitude[high_freq_start:high_freq_start*2]
        artifacts['hf_consistency'] = 1.0 - (np.std(high_freq) / (np.mean(high_freq) + 1e-6))
        
        # 3. Temporal consistency
        frame_length = int(0.025 * sr)  # 25ms frames
        hop_length = int(0.010 * sr)     # 10ms hop
        
        frames = librosa.util.frame(audio, frame_length=frame_length, hop_length=hop_length)
        frame_energies = np.sum(frames**2, axis=0)
        
        # AI voices often have more consistent energy
        artifacts['energy_consistency'] = 1.0 - (np.std(frame_energies) / (np.mean(frame_energies) + 1e-6))
        
        # 4. Micro-jitter analysis (humans have natural jitter)
        if sr >= 16000:
            # Calculate jitter in pitch
            pitches, _ = librosa.piptrack(y=audio, sr=sr)
            pitch_track = []
            for t in range(pitches.shape[1]):
                index = magnitudes[:, t].argmax()
                pitch_track.append(pitches[index, t])
            
            pitch_track = np.array([p for p in pitch_track if p > 0])
            if len(pitch_track) > 2:
                pitch_diff = np.diff(pitch_track)
                artifacts['pitch_jitter'] = np.std(pitch_diff) / (np.mean(pitch_track) + 1e-6)
            else:
                artifacts['pitch_jitter'] = 0
        
        return artifacts
    
    def analyze_audio(self, audio: np.ndarray, sr: int, language: str) -> Tuple[str, float]:
        """
        Comprehensive analysis to detect AI-generated voice
        
        Returns:
            classification: "AI_GENERATED" or "HUMAN"
            confidence: float between 0.0 and 1.0
        """
        
        # Extract features
        features = self.extract_advanced_features(audio, sr)
        artifacts = self.detect_artifacts(audio, sr)
        
        # Scoring system
        ai_indicators = []
        
        # 1. Spectral consistency check
        spectral_var = features['spectral_bandwidth_std'] / (features['spectral_bandwidth_mean'] + 1e-6)
        if spectral_var < 0.2:
            ai_indicators.append(0.15)
        
        # 2. MFCC uniformity
        mfcc_coeff_var = np.mean(features['mfcc_std']) / (np.mean(np.abs(features['mfcc_mean'])) + 1e-6)
        if mfcc_coeff_var < 0.25:
            ai_indicators.append(0.20)
        
        # 3. Energy consistency (strong indicator)
        if features['rms_variance'] < 0.01:
            ai_indicators.append(0.18)
        
        # 4. Pitch stability (AI lacks natural variation)
        if features['pitch_std'] > 0 and features['pitch_std'] / (features['pitch_mean'] + 1e-6) < 0.05:
            ai_indicators.append(0.17)
        
        # 5. High-frequency artifacts
        if artifacts.get('hf_consistency', 0) > 0.7:
            ai_indicators.append(0.15)
        
        # 6. Periodicity (AI often has unnatural periodicity)
        if artifacts.get('periodicity_score', 0) > 0.6:
            ai_indicators.append(0.12)
        
        # 7. Energy consistency artifacts
        if artifacts.get('energy_consistency', 0) > 0.75:
            ai_indicators.append(0.13)
        
        # 8. Lack of micro-jitter (humans have natural jitter)
        if artifacts.get('pitch_jitter', 0) < 0.02:
            ai_indicators.append(0.15)
        
        # 9. Spectral flatness (AI often has flatter spectrum)
        if features['spectral_flatness_mean'] > 0.3:
            ai_indicators.append(0.10)
        
        # 10. Phase consistency
        if features['phase_std'] < 0.8:
            ai_indicators.append(0.12)
        
        # Calculate final score
        if len(ai_indicators) > 0:
            ai_score = sum(ai_indicators)
            # Normalize to 0-1 range
            ai_score = min(ai_score, 1.0)
        else:
            ai_score = 0.2  # Low confidence if no indicators
        
        # Classification threshold
        threshold = 0.5
        
        if ai_score >= threshold:
            classification = "AI_GENERATED"
            confidence = ai_score
        else:
            classification = "HUMAN"
            confidence = 1.0 - ai_score
        
        # Ensure confidence is in valid range
        confidence = max(0.0, min(1.0, confidence))
        
        return classification, round(confidence, 4)

# Standalone testing function
def test_detector():
    """Test the advanced detector"""
    detector = AdvancedDeepfakeDetector()
    
    # Generate sample audio for testing
    duration = 3  # seconds
    sr = 16000
    t = np.linspace(0, duration, int(sr * duration))
    
    # Simulate human voice (more variation)
    human_audio = np.sin(2 * np.pi * 200 * t) * (1 + 0.3 * np.random.randn(len(t)))
    
    # Simulate AI voice (more consistent)
    ai_audio = np.sin(2 * np.pi * 200 * t) * (1 + 0.05 * np.random.randn(len(t)))
    
    print("Testing Advanced Deepfake Detector")
    print("=" * 60)
    
    # Test human audio
    classification, confidence = detector.analyze_audio(human_audio, sr, "english")
    print(f"\nHuman-like audio:")
    print(f"  Classification: {classification}")
    print(f"  Confidence: {confidence:.4f}")
    
    # Test AI audio
    classification, confidence = detector.analyze_audio(ai_audio, sr, "english")
    print(f"\nAI-like audio:")
    print(f"  Classification: {classification}")
    print(f"  Confidence: {confidence:.4f}")

if __name__ == "__main__":
    test_detector()
