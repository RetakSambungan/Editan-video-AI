const photo = document.getElementById("photo");
const audio = document.getElementById("audio");
const preview = document.getElementById("preview");
const createBtn = document.getElementById("createBtn");
const status = document.getElementById("status");
const result = document.getElementById("result");

photo.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    preview.src = URL.createObjectURL(file);
    preview.style.display = "block";
});

createBtn.addEventListener("click", async function () {

    if (!photo.files[0]) {
        alert("Pilih foto terlebih dahulu.");
        return;
    }

    if (!audio.files[0]) {
        alert("Pilih audio terlebih dahulu.");
        return;
    }

    const formData = new FormData();

    formData.append("photo", photo.files[0]);
    formData.append("audio", audio.files[0]);

    createBtn.disabled = true;
    status.innerText = "Sedang memproses...";

    try {

        const response = await fetch("/create-video", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Gagal membuat video");
        }

        const data = await response.json();

        if (data.video) {

            result.src = data.video;
            result.style.display = "block";

            status.innerText = "Video berhasil dibuat!";

        } else {

            status.innerText = "Video belum tersedia.";

        }

    } catch (error) {

        console.error(error);
        status.innerText =
            "Terjadi kesalahan. Pastikan server berjalan.";

    }

    createBtn.disabled = false;
});