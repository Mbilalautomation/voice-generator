import asyncio
import edge_tts
import streamlit as st

st.set_page_config(page_title="Team Voice Generator", page_icon="🎙️")
st.title("🎙️ Free Team Voice-Over Tool")
st.write("Apni team ke liye high-quality free voice-over generate karein.")

# Text Input
text_input = st.text_area(
    "Text yahan likhein:",
    height=150,
    placeholder="Yahan apna text enter karein...",
)

# Voice Options (Popular realistic voices)
voices = {
    "English (US) - Guy (Male)": "en-US-GuyNeural",
    "English (US) - Jenny (Female)": "en-US-JennyNeural",
    "English (UK) - Ryan (Male)": "en-GB-RyanNeural",
    "English (UK) - Sonia (Female)": "en-GB-SoniaNeural",
    "Urdu (Pakistan) - Asad (Male)": "ur-PK-AsadNeural",
    "Urdu (Pakistan) - Uzma (Female)": "ur-PK-UzmaNeural",
    "Hindi (India) - Madhur (Male)": "hi-IN-MadhurNeural",
    "Hindi (India) - Swara (Female)": "hi-IN-SwaraNeural",
}

selected_voice_label = st.selectbox(
    "Voice Select Karein:", list(voices.keys())
)
selected_voice = voices[selected_voice_label]


# TTS Conversion Function
async def generate_audio(text, voice):
    output_file = "output.mp3"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file


# Generate Button
if st.button("Generate Voice Over 🚀"):
    if not text_input.strip():
        st.error("Meharbani karke pehle kuch text likhein!")
    else:
        with st.spinner("Voice generate ho rahi hai..."):
            asyncio.run(generate_audio(text_input, selected_voice))
            st.success("Voice Over Tayyar Hai!")

            # Audio Player & Download Button
            audio_bytes = open("output.mp3", "rb").read()
            st.audio(audio_bytes, format="audio/mp3")
            st.download_button(
                label="📥 Download Audio (MP3)",
                data=audio_bytes,
                file_name="voice_over.mp3",
                mime="audio/mp3",
            )
