from fastapi import APIRouter, UploadFile, File
import shutil
import os

from .services.transcriber import transcribe_audio
from .services.summarizer import summarize_text

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "audio")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/transcribe")
async def transcribe_meeting(file: UploadFile = File(...)):

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcript = transcribe_audio(file_location)

    summary = summarize_text(transcript)

    return {
        "filename": file.filename,
        "transcript": transcript,
        "summary": summary
    }