import streamlit as st
import settings
from streamlit_extras.switch_page_button import switch_page
from transformers import pipeline
import soundfile as sf
import io
from pydub import AudioSegment
import librosa

settings.init()

st.set_page_config(
    page_title="8drtna",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Load Whisper model and processor
@st.cache_resource
def load_whisper_model():
    transcriber = pipeline(task = "automatic-speech-recognition", model="openai/whisper-small", generate_kwargs={"task": "transcribe"})
    return transcriber

transcriber = load_whisper_model()

def transcribe_audio(audio_bytes):
    try:
        # Convert audio bytes to AudioSegment
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # Export audio to WAV format in-memory
        audio_wav_io = io.BytesIO()
        audio.export(audio_wav_io, format="wav")
        audio_wav_io.seek(0)
        
        # Load audio data as mono and resample to 16kHz
        y, sr = librosa.load(audio_wav_io, sr=None)
        y_resampled = librosa.resample(y, orig_sr=sr, target_sr=16000)
        
        # Transcribe audio
        result = transcriber(y_resampled, return_timestamps=True, generate_kwargs={"task": "transcribe", "language": "en"})
        transcription = result["text"]
        return transcription
    except FileNotFoundError:
        st.error("Error: File not found.")
    except ValueError as e:
        st.error(f"Error processing audio: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

def main_page():
    """Displays the main page content"""
    st.title("Welcome to 8drtna")
    
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

        if uploaded_file is not None:
            try:
                audio_bytes = uploaded_file.read()
                st.audio(audio_bytes, format='audio/wav')

                st.write("Transcript:")
                transcript = transcribe_audio(audio_bytes)
                if transcript:
                    st.write(transcript)
                else:
                    st.error("Transcription failed.")
            except Exception as e:
                st.error(f"Error uploading file: {e}")
    else:
        st.write("Please log in to access the content.")
        login_button = st.button("Login", type="primary", use_container_width=True)
        register_button = st.button("Register", use_container_width=True)
        
        if register_button:
            switch_page("register page")  # Replace with the actual page name
        elif login_button:
            switch_page("login page")  # Replace with the actual page name

# Call the main_page function to display the content
main_page()
