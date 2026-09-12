import streamlit as st
import replicate
import os
import tempfile

st.set_page_config(page_title="AI Video Generator")
st.title("🎬 Bisa Bicara")

os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

image_file = st.file_uploader("1. Upload Foto Wajah", type=["jpg", "jpeg", "png"])
audio_file = st.file_uploader("2. Upload Audio MP3", type=["mp3", "wav"])

def save_temp_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
        tmp.write(uploaded_file.getvalue())
        return tmp.name

if st.button("Generate Video"):
    if image_file and audio_file:
        with st.spinner("⏳ Lagi bikin video... 2-3 menit"):
            try:
                image_path = save_temp_file(image_file)
                audio_path = save_temp_file(audio_file)

                output = replicate.run(
                    "mostudio/talking-photo:v2",
                    input={
                        "image": open(image_path, "rb"),
                        "audio": open(audio_path, "rb")
                    }
                )
                st.success("Selesai!")
                st.video(output)

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Upload foto + audio dulu ya")
