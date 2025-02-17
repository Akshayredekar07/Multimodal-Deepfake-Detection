# utils.py
import librosa
import numpy as np
import torch

def preprocess_audio(file_path, target_duration=15.0, target_sr=44100, n_mfcc=40):
    """
    Preprocess an audio file by loading, resampling, normalizing, and extracting MFCC features.

    Args:
        file_path (str): Path to the audio file.
        target_duration (float): Target duration of the audio in seconds.
        target_sr (int): Target sample rate.
        n_mfcc (int): Number of MFCC features to extract.

    Returns:
        torch.Tensor: A tensor of shape (1, seq_len, n_mfcc) containing MFCC features.
    """
    try:
        # Load audio file
        audio, sr = librosa.load(file_path, sr=None, mono=True)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

    # Resample audio if necessary
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)

    # Pad or truncate audio to target duration
    target_length = int(target_duration * target_sr)
    if len(audio) < target_length:
        audio = np.pad(audio, (0, target_length - len(audio)), mode='constant')
    else:
        audio = audio[:target_length]

    # Normalize audio
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))

    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=audio, sr=target_sr, n_mfcc=n_mfcc)
    return torch.tensor(mfcc.T, dtype=torch.float32).unsqueeze(0)  # Add batch dimension