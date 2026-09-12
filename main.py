import os
import tempfile

from flask import Flask, render_template, request, jsonify
import replicate


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    if "photo" not in request.files:
        return jsonify({
            "error": "Foto belum dipilih"
        }), 400

    if "audio" not in request.files:
        return jsonify({
            "error": "Audio belum dipilih"
        }), 400

    photo = request.files["photo"]
    audio = request.files["audio"]

    if photo.filename == "":
        return jsonify({
            "error": "Nama file foto kosong"
        }), 400

    if audio.filename == "":
        return jsonify({
            "error": "Nama file audio kosong"
        }), 400


    try:

        # Simpan sementara file yang dikirim pengguna
        photo_file = tempfile.NamedTemporaryFile(
            suffix=".jpg",
            delete=False
        )

        audio_file = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        photo.save(photo_file.name)
        audio.save(audio_file.name)

        photo_file.close()
        audio_file.close()


        # Jalankan SadTalker
        output = replicate.run(
            "cjwbw/sadtalker:a519cc0cfebaaeade068b23899165a11ec76aaa1d2b313d40d214f204ec957a3",

            input={
                "source_image": open(photo_file.name, "rb"),
                "driven_audio": open(audio_file.name, "rb"),

                "use_enhancer": True,
                "use_eyeblink": True,

                "pose_style": 0,
                "expression_scale": 1,

                "preprocess": "crop",
                "size_of_image": 256,

                "facerender": "facevid2vid",
                "still_mode": True
            }
        )


        # URL video hasil
        video_url = output.url


        # Hapus file sementara
        try:
            os.remove(photo_file.name)
            os.remove(audio_file.name)
        except:
            pass


        return jsonify({
            "video": video_url
        })


    except Exception as e:

        print("ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
