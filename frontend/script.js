document.getElementById("upload-btn").addEventListener("click", function () {
    const fileInput = document.getElementById("excel-upload");
    const statusText = document.getElementById("upload-status");

    if (fileInput.files.length === 0) {
        statusText.innerText = "❌ Please select a file first.";
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    fetch("http://127.0.0.1:5000/api/upload-excel", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        statusText.innerText = data.message;
    })
    .catch(error => {
        console.error("Error:", error);
        statusText.innerText = "❌ Failed to upload file.";
    });
});
