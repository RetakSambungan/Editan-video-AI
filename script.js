const photoInput = document.getElementById("photoInput");
const audioInput = document.getElementById("audioInput");

const photoPreview = document.getElementById("photoPreview");
const audioPreview = document.getElementById("audioPreview");
const audioName = document.getElementById("audioName");

const generateButton = document.getElementById("generateButton");
const status = document.getElementById("status");

const resultCard = document.getElementById("resultCard");
const resultVideo = document.getElementById("resultVideo");
const downloadButton = document.getElementById("downloadButton");


// =========================
// PREVIEW FOTO
// =========================

photoInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    const imageURL = URL.createObjectURL(file);

    photoPreview.innerHTML = `
        <img src="${imageURL}" alt="Foto yang dipilih">
    `;
});


// =========================
// PREVIEW AUDIO
// =========================

audioInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    audioName.textContent = "Audio: " + file.name;

    const audioURL = URL.createObjectURL(file);

    audioPreview.src = audioURL;
    audioPreview.style.display = "block";
});


// =========================
// BUAT FOTO BERBICARA
// =========================

generateButton.addEventListener("click", async function () {

    const photo = photoInput.files[0];
    const audio = audioInput.files[0];

    if (!photo) {
        alert("Silakan pilih foto terlebih dahulu.");
        return;
    }

    if (!audio) {
        alert("Silakan pilih audio terlebih dahulu.");
        return;
    }


    generateButton.disabled = true;

    status.textContent =
        "⏳ Sedang memproses foto dan audio...";

    resultCard.style.display = "none";


    const formData = new FormData();

    formData.append("photo", photo);
    formData.append("audio", audio);


    try {

        const response = await fetch("/generate", {
            method: "POST",
            body: formData
        });


        if (!response.ok) {

            const errorText = await response.text();

            throw new Error(
                errorText || "Gagal membuat video."
            );
        }


        const data = await response.json();


        if (!data.video) {

            throw new Error(
                "Server tidak mengembalikan video."
            );
        }


        // Tampilkan hasil video
        resultVideo.src = data.video;

        downloadButton.href = data.video;

        resultCard.style.display = "block";

        status.textContent =
            "✅ Video berhasil dibuat!";


        resultVideo.load();

    } catch (error) {

        console.error(error);

        status.textContent =
            "❌ Gagal membuat video.";

        alert(
            "Terjadi kesalahan:\n" +
            error.message
        );

    } finally {

        generateButton.disabled = false;
    }

});
