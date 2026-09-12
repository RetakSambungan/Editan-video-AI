import streamlit as st
import replicate
import tempfile
import os

st.set_page_config(page_title="AI Video Generator")
st.title("🎬 AI Video Generator")
st.write("Upload foto + audio buat bikin video AI")

# Ambil token dari Secrets
try:
    REPLICATE_API_TOKEN = st.secrets["REPLICATE_API_TOKEN"]
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
except:
    st.warning("Belum set REPLICATE_API_TOKEN di Secrets")

image_file = st.file_uploader("1. Upload Foto", type=["jpg", "jpeg", "png"])
audio_file = st.file_uploader("2. Upload Audio", type=["mp3", "wav"])

if st.button("Generate Video"):
    if image_file and audio_file:
        with st.spinner("Lagi bikin video... tunggu 1-2 menit"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_img:
                tmp_img.write(image_file.read())
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_audio:
                tmp_audio.write(audio_file.read())
            
            output = replicate.run(
                "kandinsky-community/kandinsky-video", # ganti sama model kamu
                input={"image": open(tmp_img.name, "rb"), "audio": open(tmp_audio.name, "rb")}
            )
            st.video(output)
            st.success("Selesai!")
    else:
        st.error("Upload foto + audio dulu ya")
