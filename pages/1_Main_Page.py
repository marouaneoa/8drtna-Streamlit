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
def load_whisper_model(language):
    model_name = "marouaneoa/whisper-small-dar" if language == "Darija" else "marouaneoa/whisper-small-kabyle"
    transcriber = pipeline("automatic-speech-recognition", model=model_name, generate_kwargs={"task": "transcribe"})
    return transcriber

def transcribe_audio(transcriber, audio_bytes, file_extension):
    try:
        # Convert audio bytes to AudioSegment
        if file_extension == "mp3":
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")
        else:
            audio = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
        
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

def upload_to_supabase(user_id, audio_bytes, filename, transcription):
    try:
        storage_response = settings.supabase_client.storage.from_("audio").upload(path=filename, file=audio_bytes, file_options={"content-type": "audio/wav"})
        
        if storage_response:
            # Get the public URL of the uploaded file
            file_url_response = settings.supabase_client.storage.from_("audio").get_public_url(filename)
            # st.write(f"File URL response: {file_url_response}")
            file_url = file_url_response
            
            if file_url:
                # Insert the transcription data into the database
                data = {
                    "user_id": user_id,
                    "file_url": file_url,
                    "transcription": transcription
                }
                db_response = settings.supabase_client.table("transcriptions").insert(data).execute()
                
                if db_response:
                    st.success("File and transcription uploaded successfully!")
                else:
                    st.error(f"Failed to upload transcription data.")
            else:
                st.error("Failed to retrieve the file URL.")
        else:
            st.error(f"Failed to upload audio file. Status code: {storage_response.get('status_code')}")
    except Exception as e:
        st.error(f"Error uploading to Supabase: {e}")

def main_page():
    """Displays the main page content"""
    st.title("Welcome to 8drtna")
    
    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user:
        language = st.selectbox("Select Language", ["Darija", "Kabyle"])

        transcriber = load_whisper_model(language)

        uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

        if uploaded_file is not None:
            try:
                file_extension = uploaded_file.name.split(".")[-1]
                audio_bytes = uploaded_file.read()
                st.audio(audio_bytes, format=f'audio/{file_extension}')

                st.write("Transcript:")
                transcript = transcribe_audio(transcriber, audio_bytes, file_extension)
                if transcript:
                    st.write(transcript)
                    # Upload the file and transcription to Supabase
                    user_id = st.session_state.user["id"]  
                    filename = f"{user_id}_{uploaded_file.name}"
                    upload_to_supabase(user_id, audio_bytes, filename, transcript)
                else:
                    st.error("Transcription failed.")
            except Exception as e:
                st.error(f"Error uploading file: {e}")
    else:
        st.write("Please log in to access the content.")
        login_button = st.button("Login", type="primary", use_container_width=True)
        register_button = st.button("Register", use_container_width=True)
        
        if register_button:
            switch_page("register page")  
        elif login_button:
            switch_page("login page")  


main_page()
