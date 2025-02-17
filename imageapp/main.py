import torch  
import torch.nn as nn  
import torchvision.models as models  
import torchvision.transforms as transforms  
from fastapi import FastAPI, File, UploadFile, HTTPException  
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.responses import HTMLResponse  
from fastapi.staticfiles import StaticFiles  
from fastapi.templating import Jinja2Templates  
from PIL import Image  
import io  
import logging  
from typing import Dict, Any  
from fastapi import Request  

# Configure logging  
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)  

class SelfAttention(nn.Module):  
    def __init__(self, input_dim, num_heads=4):  
        super(SelfAttention, self).__init__()  
        self.attn = nn.MultiheadAttention(embed_dim=input_dim, num_heads=num_heads, batch_first=True)  

    def forward(self, x):  
        attn_output, _ = self.attn(x, x, x)  
        return attn_output.mean(dim=1)  

class FeaturePooling(nn.Module):  
    def __init__(self):  
        super(FeaturePooling, self).__init__()  
        self.global_avg = nn.AdaptiveAvgPool2d((1, 1))  
        self.global_max = nn.AdaptiveMaxPool2d((1, 1))  

    def forward(self, x):  
        avg_pooled = self.global_avg(x)  
        max_pooled = self.global_max(x)  
        return torch.cat([avg_pooled, max_pooled], dim=1)  

class EfficientNetV2_LSTM(nn.Module):  
    def __init__(self):  
        super(EfficientNetV2_LSTM, self).__init__()  
        efficientnet = models.efficientnet_b2(weights='DEFAULT')  # Load pretrained weights if available  
        self.feature_extractor = nn.Sequential(*list(efficientnet.features))  
        self.feature_size = 1408  

        self.feature_pooling = FeaturePooling()  
        self.lstm = nn.LSTM(input_size=self.feature_size * 2, hidden_size=256, num_layers=1, batch_first=True, bidirectional=True)  
        self.attention = SelfAttention(input_dim=512)  
        self.dropout = nn.Dropout(p=0.3)  
        self.batch_norm = nn.BatchNorm1d(512)  
        self.classifier = nn.Linear(512, 1)  

    def forward(self, x):  
        features = self.feature_extractor(x)  
        pooled_features = self.feature_pooling(features)  
        pooled_features = pooled_features.squeeze(-1).squeeze(-1)  
        pooled_features = pooled_features.unsqueeze(1)  
        
        lstm_output, _ = self.lstm(pooled_features)  
        attended_features = self.attention(lstm_output)  
        attended_features = self.dropout(attended_features)  
        attended_features = self.batch_norm(attended_features)  
        output = self.classifier(attended_features).squeeze(dim=1)  
        return output  

app = FastAPI(  
    title="Deepfake Detection API",  
    description="API for detecting deepfake images using EfficientNetV2 with LSTM",  
    version="1.0.0"  
)  

app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["*"],  # In production, specify allowed origins  
    allow_credentials=True,  
    allow_methods=["*"],  
    allow_headers=["*"],  
)  

transform = transforms.Compose([  
    transforms.Resize((260, 260)),  
    transforms.ToTensor(),  
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])  
])  

# Initialize model  
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  
model = EfficientNetV2_LSTM()  
model.load_state_dict(torch.load("best_model_gpu.pth", map_location=device))  
model.to(device)  
model.eval()  
logger.info(f"Model loaded successfully on {device}")  

def process_image(image: Image.Image) -> torch.Tensor:  
    img_tensor = transform(image)  
    img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension  
    return img_tensor.to(device)  

def validate_image(image: Image.Image) -> bool:  
    return image.mode in ['RGB', 'RGBA']  

@app.get("/", response_class=HTMLResponse)  # Serve HTML page at root  
async def read_root(request: Request) -> HTMLResponse:  
    return templates.TemplateResponse("index.html", {"request": request})   

@app.post("/predict")  
async def predict(file: UploadFile = File(...)) -> Dict[str, Any]:  
    try:  
        if file.content_type is None or not file.content_type.startswith('image/'):  
            raise HTTPException(status_code=400, detail="File must be an image")  

        image_data = await file.read()  
        image = Image.open(io.BytesIO(image_data)).convert('RGB')  

        if not validate_image(image):  
            raise HTTPException(status_code=400, detail="Invalid image format")  

        image_tensor = process_image(image)  

        with torch.no_grad():  
            output = model(image_tensor)  
            probability = torch.sigmoid(output).item()  
            prediction = "Fake" if probability > 0.5 else "Real"  

        return {  
            "filename": file.filename,  
            "prediction": prediction,  
            "confidence": float(probability)  
        }  

    except Exception as e:  
        logger.error(f"Error processing request: {e}")  
        raise HTTPException(status_code=500, detail="Internal server error")  

# Mount static files and set up Jinja2 templates  
app.mount("/static", StaticFiles(directory="static"), name="static")  
templates = Jinja2Templates(directory="templates")  

if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host="0.0.0.0", port=8000)