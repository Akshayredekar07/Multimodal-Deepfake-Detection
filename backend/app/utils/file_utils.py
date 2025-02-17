import os

ALLOWED_EXTENSIONS = {
    "image": ["jpg", "jpeg", "png"],
    "audio": ["mp3", "wav", "ogg"],
    "video": ["mp4", "avi", "mov"],
}

def get_upload_path(file_type: str) -> str:
    """Returns the upload directory based on file type."""
    return os.path.join("uploads", file_type)

def allowed_file_types(filename: str, file_type: str) -> bool:
    """Check if uploaded file has an allowed extension."""
    ext = filename.split(".")[-1].lower()
    return ext in ALLOWED_EXTENSIONS.get(file_type, [])
