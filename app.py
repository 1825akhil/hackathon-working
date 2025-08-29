import streamlit as st
from gtts import gTTS
import base64
import os

# -------------------------------
# Title and description
# -------------------------------
st.set_page_config(page_title="EchoVerse", layout="centered")
st.title("🎧 EchoVerse - AI Audiobook Creator")
st.write("Transform your text into expressive, natural-sounding audio with customizable tones.")

# -------------------------------
# File upload or text input
# -------------------------------
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
text_input = ""

if uploaded_file:
    text_input = uploaded_file.read().decode("utf-8")
else:
    text_input = st.text_area("Or paste your text below:", height=200)

# -------------------------------
# Tone Selection
# -------------------------------
tone = st.radio(
    "Select Tone for Narration:",
    ["Neutral", "Suspenseful", "Inspiring"],
    index=0
)

# -------------------------------
# Tone-based rewriting (placeholder)
# -------------------------------
def rewrite_text(original_text, tone):
    # 🔹 Placeholder for IBM Watsonx Granite LLM integration
    if tone == "Neutral":
        return original_text
    elif tone == "Suspenseful":
        return "🔹 [Suspenseful Rewrite] " + original_text
    elif tone == "Inspiring":
        return "✨ [Inspiring Rewrite] " + original_text
    return original_text

# -------------------------------
# Generate Audio
# -------------------------------
if st.button("Generate Audio"):
    if text_input.strip():
        rewritten_text = rewrite_text(text_input, tone)

        # Generate speech with gTTS
        tts = gTTS(text=rewritten_text, lang="en")
        filename = "output.mp3"
        tts.save(filename)

        # Play audio in app
        audio_file = open(filename, "rb").read()
        st.audio(audio_file, format="audio/mp3")

        # Download link
        b64 = base64.b64encode(audio_file).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">⬇️ Download Audio</a>'
        st.markdown(href, unsafe_allow_html=True)

        # Show rewritten text for reference
        with st.expander("📖 View Rewritten Text"):
            st.write(rewritten_text)
    else:
        st.warning("⚠️ Please provide some text to generate audio.")

