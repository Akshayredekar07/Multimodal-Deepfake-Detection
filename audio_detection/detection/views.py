from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import JsonResponse
import torch
from .model import model
from .utils import preprocess_audio

def home(request):
    return render(request, "index.html")

def predict(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        file_path = default_storage.save("temp_audio.wav", file)
        
        features = preprocess_audio(file_path)
        if features is None:
            return JsonResponse({"error": "Failed to preprocess audio file"}, status=400)

        features = features.to(torch.device("cuda" if torch.cuda.is_available() else "cpu"))

        with torch.no_grad():
            model_output = model(features).cpu().detach().numpy().tolist()

        return JsonResponse({"prediction": model_output})

    return JsonResponse({"error": "Invalid request"}, status=400)
