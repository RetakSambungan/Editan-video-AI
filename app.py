from flask import Flask, request, jsonify, send_from_directory
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)


@app.route("/create-video", methods=["POST"])
def create_video():

    photo = request.files.get("photo")
    audio = request.files.get("audio")

    if not photo or not audio:
        return jsonify({
            "error": "Foto dan audio wajib dipilih"
        }), 400

    uid = str(uuid.uuid4())

    photo_path = os.path.join(
        UPLOAD_FOLDER,
        uid + "_photo.jpg"
    )

    audio_path = os.path.join(
        UPLOAD_FOLDER,
        uid + "_audio.mp3"
    )

    photo.save(photo_path)
    audio.save(audio_path)

    # ==========================================
    # TEMPAT AI LIP-SYNC AKAN DIPASANG
    # ==========================================

    return jsonify({
        "message": "Foto dan audio berhasil diterima",
        "photo": photo_path,
        "audio": audio_path
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )