import asyncio
import random
import urllib.parse
import edge_tts
import requests
import streamlit as st

# Page Config
st.set_page_config(
    page_title="Team AI Production Studio", page_icon="🎨", layout="wide"
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
    .stTextArea textarea, .stTextInput input, .stSelectbox div { 
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
    tab1, tab2 = st.tabs(
        ["🎙️ Voice Over Studio", "🎨 8K Ultra-HD Visual Generator"]
    )

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

    # --- TAB 2: ULTRA HD VISUAL GENERATOR ---
    with tab2:
        st.subheader("🖼️ FLUX 8K Ultra-HD Image Studio")
        st.caption(
            "High-resolution professional AI images generate karein har format mein."
        )

        p_col1, p_col2 = st.columns([2, 1])

        with p_col1:
            prompt_input = st.text_area(
                "Visual Description (Prompt)",
                height=160,
                placeholder="e.g. A futuristic lion king with a glowing crown standing on a peak, hyperrealistic, dramatic volumetric lighting",
            )

        with p_col2:
            ratio_option = st.selectbox(
                "📐 Aspect Ratio / Format",
                [
                    "16:9 (Landscape - YouTube / Web)",
                    "9:16 (Vertical - Reels / Shorts / Stories)",
                    "1:1 (Square - Instagram / Profile)",
                    "4:3 (Standard Banner)",
                    "21:9 (Ultrawide Cinematic)",
                ],
            )

            num_images = st.slider(
                "🖼️ Number of Variations",
                min_value=2,
                max_value=4,
                value=2,
                step=1,
            )

        # Aspect Ratio Dimensions Mapping
        dimensions = {
            "16:9 (Landscape - YouTube / Web)": (1280, 720),
            "9:16 (Vertical - Reels / Shorts / Stories)": (720, 1280),
            "1:1 (Square - Instagram / Profile)": (1024, 1024),
            "4:3 (Standard Banner)": (1152, 864),
            "21:9 (Ultrawide Cinematic)": (1344, 576),
        }

        width, height = dimensions[ratio_option]

        if st.button("✨ Generate 8K Ultra-HD Visuals"):
            if not prompt_input.strip():
                st.warning("Pehle prompt input daalein!")
            else:
                # Automatic Prompt Enhancement for 8K/4K Quality
                enhanced_prompt = f"{prompt_input}, 8k resolution, hyperrealistic, highly detailed, photorealistic, sharp focus, 4k masterwork"
                encoded_prompt = urllib.parse.quote(enhanced_prompt)

                cols = st.columns(num_images)

                for i in range(num_images):
                    with cols[i]:
                        seed = random.randint(1000, 999999)
                        img_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&seed={seed}&nologo=true"

                        with st.spinner(f"Rendering Image {i+1} (8K)..."):
                            try:
                                res = requests.get(img_url, timeout=30)
                                if res.status_code == 200:
                                    st.image(
                                        res.content,
                                        caption=f"Variation {i+1} ({width}x{height})",
                                        use_container_width=True,
                                    )
                                    st.download_button(
                                        label=f"📥 Download Variation {i+1}",
                                        data=res.content,
                                        file_name=f"ultra_hd_visual_{i+1}.png",
                                        mime="image/png",
                                        key=f"dl_{i}",
                                    )
                                else:
                                    st.error(
                                        f"Failed to generate variation {i+1}"
                                    )
                            except Exception as e:
                                st.error(f"Error loading image: {e}")
