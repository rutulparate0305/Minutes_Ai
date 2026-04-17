from fastapi import APIRouter, UploadFile, File, Depends
import shutil
import os
import json

from sqlalchemy.orm import Session

from .services.transcriber import transcribe_audio
from .services.summarizer import summarize_text
from .services.summarizer import extract_speakers, extract_action_items
from .database import SessionLocal
from .models import Meeting


router = APIRouter()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "audio")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/transcribe")
async def transcribe_meeting(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    from app.services.speaker_diarization import diarize_and_transcribe
    transcript = diarize_and_transcribe(file_location)

    summary = summarize_text(transcript)

    speakers = extract_speakers(transcript)

    action_items = extract_action_items(transcript)


    meeting_record = Meeting(
        filename=file.filename,
        transcript=transcript,
        summary=summary,
        speakers=json.dumps(speakers),    
        action_items=json.dumps(action_items)  
    )

    db.add(meeting_record)
    db.commit()
    db.refresh(meeting_record)


    return {
        "filename": file.filename,
        "transcript": transcript,
        "summary": summary,
        "speakers": speakers,
        "action_items": action_items
    }