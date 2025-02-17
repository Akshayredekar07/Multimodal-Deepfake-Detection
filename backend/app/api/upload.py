
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.file_service import save_uploaded_file

router = APIRouter(prefix="/upload", tags=["Upload"])

# Upload Image
@router.post("/image/")
async def upload_image(file: UploadFile = File(...)):
    return await save_uploaded_file(file, "image")

# Upload Audio
@router.post("/audio/")
async def upload_audio(file: UploadFile = File(...)):
    return await save_uploaded_file(file, "audio")

# Upload Video
@router.post("/video/")
async def upload_video(file: UploadFile = File(...)):
    return await save_uploaded_file(file, "video")



from fastapi import APIRouter, File, UploadFile
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "app/database/uploads"  # Ensure this folder exists

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file name")
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "message": "File uploaded successfully", "path": file_path}
