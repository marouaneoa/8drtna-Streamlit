import streamlit as st
import settings
from streamlit_extras.switch_page_button import switch_page
from transformers import pipeline
import soundfile as sf
import io

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
    transcriber = pipeline(model="openai/whisper-small")
    return transcriber

transcriber = load_whisper_model()

def transcribe_audio(audio_bytes):
    # Load audio data
    audio_input, sample_rate = sf.read(io.BytesIO(audio_bytes))
    # Transcribe audio
    transcription = transcriber(audio_input, sampling_rate=sample_rate)["text"]
    return transcription

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
