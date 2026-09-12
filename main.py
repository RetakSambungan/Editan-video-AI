import streamlit as st
import replicate
import os

st.title("🎬 AI Video Generator")

os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

image_file = st.file_uploader("Upload Foto", type=["jpg", "jpeg", "png"])
audio_file = st.file_uploader("Upload Audio", type=["mp3", "wav"])

if st.button("Generate Video"):
    if image_file and audio_file:
        with st.spinner("Lagi bikin video... 2-3 menit"):
            output = replicate.run(
                "lucataco/animate-diff", 
                input={"image": image_file, "audio": audio_file}
            )
            st.video(output[0])
    else:
        st.warning("Upload foto + audio dulu")
