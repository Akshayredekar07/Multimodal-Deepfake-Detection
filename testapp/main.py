# # main.py
# from fastapi import FastAPI, File, UploadFile, HTTPException
# import torch
# from model import BiLSTM_Attention  # Ensure BiLSTM_Attention is explicitly imported
# from utils import preprocess_audio  # Import the feature extraction function

# # Initialize FastAPI app
# app = FastAPI()

# # Check device (CUDA or CPU)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Load the model
# model_path = "best_model_gpu.pth"
# input_dim = 40  # Ensure this matches the input dimension of your model
# model = BiLSTM_Attention(input_dim=input_dim).to(device)

# # Load model state dictionary
# try:
#     model.load_state_dict(torch.load(model_path, map_location=device), strict=False)
#     model.eval()  # Set model to evaluation mode
#     print("✅ Model loaded successfully!")
# except Exception as e:
#     print(f"⚠️ Error loading model: {e}")

# # Define a simple route to check the API
# @app.get("/")
# def home():
#     return {"message": "FastAPI is running with BiLSTM_Attention model!"}

# # Define a prediction endpoint for audio files
# @app.post("/predict/")
# async def predict(file: UploadFile = File(...)):
#     try:
#         # Save the uploaded file temporarily
#         with open("temp_audio.wav", "wb") as buffer:
#             buffer.write(await file.read())

#         # Preprocess the audio file and extract features
#         features = preprocess_audio("temp_audio.wav")
#         if features is None:
#             raise HTTPException(status_code=400, detail="Failed to preprocess audio file.")

#         # Move features to the appropriate device
#         features = features.to(device)

#         # Perform inference
#         with torch.no_grad():  # Disable gradient calculation for inference
#             model_output = model(features).cpu().detach().numpy().tolist()

#         return {"prediction": model_output}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
import torch
from utils import preprocess_audio  # Import the feature extraction function

# Define the BiLSTM_Attention class
class BiLSTM_Attention(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim=128, num_layers=3, num_classes=1, dropout_rate=0.3):
        super(BiLSTM_Attention, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        # BiLSTM Layer with Layer Normalization
        self.lstm = torch.nn.LSTM(input_dim, hidden_dim, num_layers=num_layers,
                                  batch_first=True, bidirectional=True, dropout=dropout_rate)
        self.layer_norm = torch.nn.LayerNorm(hidden_dim * 2)  # Normalize output

        # Scaled Dot-Product Attention
        self.attention = ScaledDotProductAttention(hidden_dim * 2)

        # Fully Connected Layers with Xavier Initialization
        self.fc1 = torch.nn.Linear(hidden_dim * 2, 128)
        self.fc2 = torch.nn.Linear(128, 64)
        self.fc3 = torch.nn.Linear(64, num_classes)

        # Activation & Regularization
        self.leaky_relu = torch.nn.LeakyReLU(0.1)
        self.dropout = torch.nn.Dropout(dropout_rate)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)  # (batch, seq_len, hidden_dim*2)
        lstm_out = self.layer_norm(lstm_out)  # Apply Layer Norm

        attn_out, attn_weights = self.attention(lstm_out)  # Apply Attention

        x = self.leaky_relu(self.fc1(attn_out))
        x = self.dropout(x)
        x = self.leaky_relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)  # No sigmoid here (for BCEWithLogitsLoss)

        return x  # Logits output (apply sigmoid during loss calculation)

# Define the ScaledDotProductAttention class
class ScaledDotProductAttention(torch.nn.Module):
    def __init__(self, hidden_dim):
        super(ScaledDotProductAttention, self).__init__()
        self.scale = torch.sqrt(torch.tensor(hidden_dim, dtype=torch.float32))
        self.softmax = torch.nn.Softmax(dim=1)

    def forward(self, lstm_output):
        attn_scores = torch.bmm(lstm_output, lstm_output.transpose(1, 2)) / self.scale  # Scaled dot product
        attn_weights = self.softmax(attn_scores[:, :, -1])  # Take last step attention
        context = torch.sum(attn_weights.unsqueeze(2) * lstm_output, dim=1)  # Weighted sum
        return context, attn_weights

# Initialize FastAPI app
app = FastAPI()

# Check device (CUDA or CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the model
model_path = "best_model_cpu.pth"
input_dim = 40  # Ensure this matches the input dimension of your model
model = BiLSTM_Attention(input_dim=input_dim).to(device)

# Load model state dictionary
try:
    model.load_state_dict(torch.load(model_path, map_location=device), strict=False)
    model.eval()  # Set model to evaluation mode
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

# Define a simple route to check the API
@app.get("/")
def home():
    return {"message": "FastAPI is running with BiLSTM_Attention model!"}

# Define a prediction endpoint for audio files
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        with open("temp_audio.wav", "wb") as buffer:
            buffer.write(await file.read())

        # Preprocess the audio file and extract features
        features = preprocess_audio("temp_audio.wav")
        if features is None:
            raise HTTPException(status_code=400, detail="Failed to preprocess audio file.")

        # Move features to the appropriate device
        features = features.to(device)

        # Perform inference
        with torch.no_grad():  # Disable gradient calculation for inference
            model_output = model(features).cpu().detach().numpy().tolist()

        return {"prediction": model_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))