import librosa
import numpy as np
import torch

def preprocess_audio(file_path, target_duration=15.0, target_sr=44100, n_mfcc=40):
    try:
        audio, sr = librosa.load(file_path, sr=None, mono=True)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)

    target_length = int(target_duration * target_sr)
    if len(audio) < target_length:
        audio = np.pad(audio, (0, target_length - len(audio)), mode='constant')
    else:
        audio = audio[:target_length]

    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))

    mfcc = librosa.feature.mfcc(y=audio, sr=target_sr, n_mfcc=n_mfcc)
    return torch.tensor(mfcc.T, dtype=torch.float32).unsqueeze(0)
