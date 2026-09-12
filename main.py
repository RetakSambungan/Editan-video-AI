import streamlit as st
import replicate
import os

st.set_page_config(page_title="AI Video Generator")
st.title("🎬 AI Video Generator")

# Ambil token dari Secrets
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

image_file = st.file_uploader("1. Upload Foto Wajah", type=["jpg", "jpeg", "png"])
audio_file = st.file_uploader("2. Upload Audio MP3", type=["mp3", "wav"])

if st.button("Generate Video"):
    if image_file is not None and audio_file is not None:
        with st.spinner("⏳ Lagi bikin video... tunggu 2-3 menit ya"):
            try:
                output = replicate.run(
                    "lucataco/animate-diff",
                    input={
                        "image": image_file,
                        "audio": audio_file,
                        "prompt": "animate the person in the image, lip sync to audio",
                        "fps": 12
                    }
                )
                st.success("Selesai!")
                st.video(output[0])
                
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Upload foto + audio dulu ya")
