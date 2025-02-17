from fastapi import FastAPI
from app.api import upload
from app.routes import audio_routes

app = FastAPI(title="Multimodal Upload API")

app.include_router(upload.router)
app.include_router(audio_routes.router, prefix="/audio", tags=["Audio"])  # Fixed router name

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Multimodal Upload Service"}
