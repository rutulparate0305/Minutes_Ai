from pyannote.audio import Pipeline
import whisper
import os

# Load diarization pipeline
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization",
    use_auth_token="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"
)

# Load Whisper model
whisper_model = whisper.load_model("base")


def diarize_and_transcribe(audio_path):
    """
    Performs speaker diarization + transcription
    Returns speaker labeled transcript
    """

    diarization = pipeline(audio_path)

    speaker_transcript = ""

    for turn, _, speaker in diarization.itertracks(yield_label=True):

        segment_audio = f"temp_segment.wav"

        os.system(
            f"ffmpeg -y -i {audio_path} -ss {turn.start} -to {turn.end} {segment_audio}"
        )

        result = whisper_model.transcribe(segment_audio)

        speaker_transcript += f"{speaker}: {result['text']}\n"

    return speaker_transcript