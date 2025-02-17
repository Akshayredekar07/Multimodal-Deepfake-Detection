import torch
from fastapi import APIRouter, File, UploadFile, HTTPException
import os
import numpy as np
from app.ml_models.audio_model import BiLSTM_Attention
from app.components.audio_features import preprocess_audio
import pickle

router = APIRouter()

# Define model path
MODEL_PATH = "app/models/audio_models/best_model_cpu.pth"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the model with feature matching
try:
    # Load the checkpoint
    checkpoint = torch.load(MODEL_PATH, map_location=device, pickle_module=pickle)
    print(checkpoint.keys())


    # Ensure model parameters match checkpoint
    input_dim = checkpoint.get("input_dim", 40)  # Default to 40 if not found
    hidden_dim = checkpoint.get("hidden_dim", 128)
    num_layers = checkpoint.get("num_layers", 3)
    num_classes = checkpoint.get("num_classes", 1)
    
    model = BiLSTM_Attention(
        input_dim=input_dim,
        hidden_dim=hidden_dim,
        num_layers=num_layers,
        num_classes=num_classes,
        dropout_rate=0.0  # Set dropout to 0 for inference
    )

    # Load the state dict
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()
except Exception as e:
    raise Exception(f"Error loading model: {str(e)}")

@router.post("/predict/")
async def predict_audio(file: UploadFile = File(...)):
    file_path = f"app/database/uploads/{file.filename}"

    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    # Extract features from the audio file
    try:
        mfcc_features, _ = preprocess_audio(file_path)  # Extract MFCC
        if mfcc_features is None or not isinstance(mfcc_features, np.ndarray):
            raise HTTPException(status_code=400, detail="Feature extraction failed or invalid data")

        # Ensure input dimension matches the model
        if mfcc_features.shape[1] != input_dim:
            raise HTTPException(status_code=400, detail=f"Feature dimension mismatch. Expected {input_dim}, got {mfcc_features.shape[1]}.")

        # Convert to PyTorch tensor and reshape
        sample_input = torch.tensor(mfcc_features, dtype=torch.float32).unsqueeze(0)  # (1, time_steps, n_mfcc)
    except Exception as e:
        return {"error": str(e)}

    # Make prediction
    with torch.no_grad():
        logits = model(sample_input.to(device))  # Forward pass
        prob = torch.sigmoid(logits).item()  # Convert to probability
        prediction = "deepfake" if prob > 0.5 else "real"

    return {
        "filename": file.filename,
        "prediction": prediction,
        "confidence": round(prob, 4)  # Limit decimal places for readability
    }
