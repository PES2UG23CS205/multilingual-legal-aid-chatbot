# app/services/audio_service.py
import whisper
import io
from gtts import gTTS
from pydub import AudioSegment
import tempfile
import os

# Load the base model, it's small, fast, and multilingual
print("🧠 Audio Service: Loading Whisper model...")
try:
    whisper_model = whisper.load_model("base")
    print("✅ Audio Service: Whisper model loaded.")
except Exception as e:
    print(f"❌ Audio Service: Failed to load Whisper model. Error: {e}")
    # You might want to handle this more gracefully, but for now, we let it raise
    raise

def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribes audio bytes to text using Whisper."""
    try:
        # Convert webm/ogg bytes from frontend to a format whisper can handle
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # Whisper works best with WAV format
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio.export(tmp.name, format="wav")
            tmp_path = tmp.name
        
        # Transcribe the temporary file
        result = whisper_model.transcribe(tmp_path, fp16=False) # fp16=False for CPU
        os.remove(tmp_path) # Clean up the temp file
        
        return result["text"]
    except Exception as e:
        print(f"Error during audio transcription: {e}")
        return ""

def text_to_speech(text: str, lang: str) -> bytes:
    """Converts text to speech audio bytes using gTTS."""
    if not text:
        return b""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception as e:
        print(f"Error during text-to-speech: {e}")
        return b""