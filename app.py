import streamlit as st
import io
import os
from huggingface_hub import InferenceClient

st.title("🎤 Human-like TTS with Hugging Face InferenceClient")

# Set your HF API key in an environment variable: HF_TOKEN
HF_API_KEY = os.getenv("HF_TOKEN")
if not HF_API_KEY:
    st.error("Please set your Hugging Face API key in the HF_TOKEN environment variable.")
    st.stop()

client = InferenceClient(
    provider="fal-ai",
    api_key=HF_API_KEY,
)

# ---------------- Streamlit Inputs ----------------
text_input = st.text_area("Enter text manually:", "The answer to the universe is 42")

uploaded_file = st.file_uploader("Or upload a TXT file:", type=["txt"])
if uploaded_file is not None:
    text_input = uploaded_file.read().decode("utf-8")
    st.success("TXT file loaded successfully!")

# Add Tone and Gender selection widgets (These won't affect the current model but can be used for other models)
st.subheader("Select Voice Parameters")

selected_gender = st.selectbox(
    "Choose a gender:",
    ("male", "female")
)

selected_tone = st.selectbox(
    "Choose a tone:",
    ("normal", "funny", "joyful", "calm", "emphatic", "angry")
)

# ---------------- TTS Generation ----------------
if st.button("Generate Speech"):
    if text_input.strip() == "":
        st.warning("Please enter some text or upload a TXT file!")
    else:
        with st.spinner("Generating speech..."):
            try:
                # Corrected: Removed unsupported 'gender' and 'tone' parameters
                audio_bytes = client.text_to_speech(
                    text_input,
                    model="nari-labs/Dia-1.6B"
                )

                audio_file = io.BytesIO(audio_bytes)

                st.success("Audio generated successfully!")
                st.audio(audio_file, format="audio/wav")
                st.download_button(
                    "⬇ Download Audio",
                    audio_file,
                    file_name="speech.wav",
                    mime="audio/wav"
                )
            except Exception as e:
                st.error(f"Failed to generate audio: {e}")