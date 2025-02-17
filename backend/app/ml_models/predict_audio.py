import torch
import torch.nn.functional as F
from app.components.audio_features import preprocess_audio

def predict_audio(file_path, model):
    """
    Predict whether the given audio file is a deepfake or real.
    Args:
        file_path (str): Path to the audio file.
        model (torch.nn.Module): Preloaded PyTorch model.
    Returns:
        dict: Prediction result with confidence score.
    """
    # Step 1: Preprocess audio
    input_tensor = preprocess_audio(file_path)  # Shape: (1, seq_len, input_dim)

    # Ensure tensor is correctly formatted
    if not isinstance(input_tensor, torch.Tensor):
        input_tensor = torch.tensor(input_tensor, dtype=torch.float32)

    # Step 2: Forward pass
    with torch.no_grad():
        logits = model(input_tensor)  # Raw model output

    # Step 3: Convert logits to probability
    prob = torch.sigmoid(logits).item()

    # Step 4: Convert probability to label
    prediction = "deepfake" if prob > 0.5 else "real"

    return {"prediction": prediction, "confidence": prob}
