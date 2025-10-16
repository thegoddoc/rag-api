from fastapi import APIRouter, File, UploadFile, HTTPException
from configs.config import rag_config
import os
from pathlib import Path


router = APIRouter(prefix="/upload", tags=["upload"])


UPLOAD_DIR = rag_config['INPUT_FOLDER']
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    # ✅ Validation: check file extension
    allowed_ext = [".txt", ".pdf", ".docx"]
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in allowed_ext:
        raise HTTPException(status_code=400, detail=f"Invalid file type: {ext}")

    # ✅ Validation: check file size (e.g., 10MB limit)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    
    # ✅ Save file
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as f:
        f.write(contents)

    return {"filename": file.filename, "size": len(contents), "path": Path(save_path).parent.name}
