import os
import numpy as np
import librosa

def preprocess_audio(file_path, target_duration=15.0, target_sr=44100, n_mfcc=40):
    """Preprocess an audio file for deepfake detection."""
    try:
        audio, sr = librosa.load(file_path, sr=None, mono=True)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None, None

    # Resample if necessary
    if sr != target_sr:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
        sr = target_sr

    # Ensure audio is exactly target_duration seconds
    target_length = int(target_duration * sr)
    if len(audio) < target_length:
        audio = np.pad(audio, (0, target_length - len(audio)), mode='constant')
    else:
        audio = audio[:target_length]

    # Normalize amplitude
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))

    # Extract MFCC features
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_mfcc)
    return mfcc.T, sr  # Transpose to get (time_steps, n_mfcc)


def process_dataset(base_dir, output_dir):
    """Process all audio files in the dataset and save preprocessed features."""
    for split in ["train", "validation", "test"]:
        split_path = os.path.join(base_dir, split)
        output_split_path = os.path.join(output_dir, split)
        os.makedirs(output_split_path, exist_ok=True)

        for category in ["real", "fake"]:
            category_path = os.path.join(split_path, category)
            output_category_path = os.path.join(output_split_path, category)
            os.makedirs(output_category_path, exist_ok=True)

            # List all .wav files
            files = [f for f in os.listdir(category_path) if f.endswith(".wav")]

            for file_name in files:
                file_path = os.path.join(category_path, file_name)
                output_file_path = os.path.join(output_category_path, file_name.replace(".wav", ".npy"))

                # Preprocess audio and extract MFCC features
                mfcc_features, _ = preprocess_audio(file_path)
                if mfcc_features is not None:
                    np.save(output_file_path, mfcc_features)  # Save the MFCC features

    print("Preprocessing complete! All files are saved in 'preprocessed_data'.")
