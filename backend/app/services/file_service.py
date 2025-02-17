import os
import shutil
from fastapi import UploadFile

UPLOAD_DIR = "app/database/uploads"  # Ensure this directory exists

async def save_uploaded_file(file: UploadFile, file_type: str):
    """Save uploaded file and return details."""
    file_type_dir = os.path.join(UPLOAD_DIR, file_type)
    os.makedirs(file_type_dir, exist_ok=True)  # Ensure subdirectory exists
    
    if file.filename is None:
        raise ValueError("Filename cannot be None")
    file_path = os.path.join(file_type_dir, file.filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "message": "File uploaded successfully", "path": file_path}
