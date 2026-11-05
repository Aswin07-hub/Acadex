
document.addEventListener("DOMContentLoaded", function () {
    const fileInput = document.getElementById("file");
    const fileNote = document.getElementById("file-note");
    const form = document.querySelector("form");

    const allowedExtensions = ["pdf", "jpg", "jpeg", "png"];
    const maxFileSize = 5 * 1024 * 1024;

    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];

        if (!file) {
            return;
        }

        const extension = file.name.split(".").pop().toLowerCase();

        if (!allowedExtensions.includes(extension)) {
            alert("Only PDF, JPG, JPEG and PNG files are allowed.");
            fileInput.value = "";
            fileNote.textContent = "Please select a valid file.";
            return;
        }

        if (file.size > maxFileSize) {
            alert("File size must not exceed 5 MB.");
            fileInput.value = "";
            fileNote.textContent = "Please select a file below 5 MB.";
            return;
        }

        fileNote.textContent = "Selected file: " + file.name;
    });

    form.addEventListener("submit", function (event) {
        if (!fileInput.files.length) {
            event.preventDefault();
            alert("Please select a document before submitting.");
        }
    });
});
