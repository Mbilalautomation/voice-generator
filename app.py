import asyncio
import xml.etree.ElementTree as ET
import edge_tts
import streamlit as st

st.set_page_config(
    page_title="ElevenVoice Studio Pro", page_icon="🎙️", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp { background-color: #0B0F17; color: #FFFFFF; }
    .stButton>button {
        background: linear-gradient(90deg, #6366F1, #A855F7);
        color: white; font-weight: bold; border-radius: 8px;
        padding: 12px; border: none; width: 100%; transition: 0.3s;
    }
    .stTextArea textarea { background-color: #161B26; color: white; border: 1px solid #2D3748; border-radius: 8px; }
    </style>
""",
    unsafe_allow_html=True,
)


def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔒 Team Access Verification")
        pass_input = st.text_input("Enter Passcode:", type="password")
        if st.button("Unlock Studio"):
            if pass_input == "team123":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("❌ Incorrect Passcode!")
        return False
    return True


if check_password():
    st.sidebar.title("🎙️ Studio Settings")
    st.sidebar.write("Logged in as **Team Member**")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title("🎙️ Pro AI Voice Studio (Expressive & Natural)")
    st.caption("Human-like emotion tuning for Hindi, Urdu & English")

    col1, col2 = st.columns([2, 1])

    with col1:
        text_input = st.text_area(
            "Text Script",
            height=250,
            placeholder="Apna script yahan likhein (Hindi / Urdu / English)...",
        )

    with col2:
        # High Quality Expressive Voices
        voices = {
            "🇮🇳 Hindi - Swara (Natural Female)": "hi-IN-SwaraNeural",
            "🇮🇳 Hindi - Madhur (Deep Male)": "hi-IN-MadhurNeural",
            "🇵🇰 Urdu - Asad (Professional Male)": "ur-PK-AsadNeural",
            "🇵🇰 Urdu - Uzma (Soft Female)": "ur-PK-UzmaNeural",
            "🇺🇸 English - Jenny (Conversational Female)": "en-US-JennyNeural",
            "🇺🇸 English - Guy (Deep Male)": "en-US-GuyNeural",
            "🇬🇧 English - Ryan (Narrative Male)": "en-GB-RyanNeural",
        }

        selected_voice_label = st.selectbox(
            "Select Voice Model", list(voices.keys())
        )
        selected_voice = voices[selected_voice_label]

        speed = st.slider("Speed / Pace", -50, 50, -5, format="%d%%")
        pitch = st.slider("Pitch / Tone", -20, 20, 0, format="%dHz")

    speed_str = f"{'+' if speed >= 0 else ''}{speed}%"
    pitch_str = f"{'+' if pitch >= 0 else ''}{pitch}Hz"

    # Function to generate expressive SSML audio
    async def generate_voice(text, voice, s, p):
        out = "speech.mp3"
        # Escape XML special characters
        safe_text = (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        # SSML Wrapper to add natural pauses and prosody
        ssml_text = f"""<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
            <voice name='{voice}'>
                <prosody rate='{s}' pitch='{p}'>
                    {safe_text}
                </prosody>
            </voice>
        </speak>"""

        comm = edge_tts.Communicate(ssml_text, voice, raw_response=False)
        await comm.save(out)
        return out

    if st.button("⚡ Generate Expressive Voice"):
        if not text_input.strip():
            st.warning("Please provide text input!")
        else:
            with st.spinner("Synthesizing emotional speech..."):
                try:
                    asyncio.run(
                        generate_voice(
                            text_input, selected_voice, speed_str, pitch_str
                        )
                    )
                    st.success("Audio Generated Successfully!")

                    audio_file = open("speech.mp3", "rb").read()
                    st.audio(audio_file, format="audio/mp3")
                    st.download_button(
                        "📥 Download MP3 Audio",
                        data=audio_file,
                        file_name="expressive_voice.mp3",
                        mime="audio/mp3",
                    )
                except Exception as e:
                    st.error(f"Error generating audio: {e}")
