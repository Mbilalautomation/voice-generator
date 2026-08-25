import asyncio
import edge_tts
from gradio_client import Client
import requests
import streamlit as st

# Page Config
st.set_page_config(
    page_title="Team AI Production Studio", page_icon="🎬", layout="wide"
)

# Custom Dark ElevenLabs Styling
st.markdown(
    """
    <style>
    .stApp { background-color: #0B0F17; color: #FFFFFF; }
    .stButton>button {
        background: linear-gradient(90deg, #6366F1, #A855F7);
        color: white; font-weight: bold; border-radius: 8px;
        padding: 12px; border: none; width: 100%; transition: 0.3s;
    }
    .stTextArea textarea, .stTextInput input { 
        background-color: #161B26; color: white; border: 1px solid #2D3748; border-radius: 8px; 
    }
    </style>
""",
    unsafe_allow_html=True,
)


# Security Passcode
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
    st.sidebar.title("🛠️ Studio Menu")
    st.sidebar.write("Logged in as: **Team Member**")
    if st.sidebar.button("Logout"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.title("🚀 Team All-In-One AI Studio")

    # Main Tabs
    tab1, tab2 = st.tabs(["🎙️ Voice Over Studio", "🎬 AI Video Generator"])

    # --- TAB 1: VOICE GENERATOR ---
    with tab1:
        st.subheader("Text-to-Speech (Multilingual & Expressive)")
        col1, col2 = st.columns([2, 1])

        with col1:
            text_input = st.text_area(
                "Voice Script",
                height=220,
                placeholder="Script yahan likhein (Hindi / Urdu / English)...",
            )

        with col2:
            voices = {
                "🇵🇰 Urdu - Asad (Professional Male)": "ur-PK-AsadNeural",
                "🇵🇰 Urdu - Uzma (Soft Female)": "ur-PK-UzmaNeural",
                "🇮🇳 Hindi - Swara (Natural Female)": "hi-IN-SwaraNeural",
                "🇮🇳 Hindi - Madhur (Deep Male)": "hi-IN-MadhurNeural",
                "🇺🇸 English - Jenny (Female)": "en-US-JennyNeural",
                "🇺🇸 English - Guy (Male)": "en-US-GuyNeural",
                "🇬🇧 English - Ryan (British Accent)": "en-GB-RyanNeural",
            }

            selected_voice = voices[
                st.selectbox("Select Voice Artist", list(voices.keys()))
            ]
            speed = st.slider("Speed / Pace", -50, 50, -5, format="%d%%")
            pitch = st.slider("Pitch / Tone", -20, 20, 0, format="%dHz")

        speed_str = f"{'+' if speed >= 0 else ''}{speed}%"
        pitch_str = f"{'+' if pitch >= 0 else ''}{pitch}Hz"

        async def generate_voice(text, voice, s, p):
            out = "speech.mp3"
            comm = edge_tts.Communicate(text, voice, rate=s, pitch=p)
            await comm.save(out)
            return out

        if st.button("⚡ Generate Voice Over"):
            if not text_input.strip():
                st.warning("Pehle text input daalein!")
            else:
                with st.spinner("Generating Voice..."):
                    asyncio.run(
                        generate_voice(
                            text_input, selected_voice, speed_str, pitch_str
                        )
                    )
                    st.success("Audio Ready!")
                    audio_bytes = open("speech.mp3", "rb").read()
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button(
                        "📥 Download MP3",
                        data=audio_bytes,
                        file_name="voiceover.mp3",
                        mime="audio/mp3",
                    )

    # --- TAB 2: REAL MP4 VIDEO GENERATOR ---
    with tab2:
        st.subheader("Text-to-Video Generator (Real MP4 Clips)")
        st.caption(
            "AI se 5-second ki real motion video generate karein (Render hone mein 1-2 minutes lag sakte hain)."
        )

        video_prompt = st.text_area(
            "Video Scene Description (English Prompt)",
            height=150,
            placeholder="e.g. A majestic lion walking in the grassland during sunset, cinematic 4k video",
        )

        if st.button("🎬 Generate Real MP4 Video"):
            if not video_prompt.strip():
                st.warning("Pehle video prompt likhein!")
            else:
                with st.spinner(
                    "🎥 Video processing ho rahi hai... Pehli baar mein 1 se 2 minute lag sakte hain!"
                ):
                    try:
                        # Hugging Face Open Source Model Client
                        client = Client("damo-vilab/modelscope-text-to-video")
                        result_path = client.predict(
                            prompt=video_prompt, api_name="/predict"
                        )

                        st.success("🎉 Video Ready!")

                        # Render MP4 Video Player
                        st.video(result_path)

                        # Download Button
                        with open(result_path, "rb") as file:
                            st.download_button(
                                label="📥 Download MP4 Video",
                                data=file,
                                file_name="ai_generated_video.mp4",
                                mime="video/mp4",
                            )
                    except Exception as e:
                        st.error(
                            f"Video model busy hai ya error aaya. Dobara try karein. Detail: {e}"
                        )
