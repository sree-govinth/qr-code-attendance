document.getElementById("start-scan").addEventListener("click", function () {
    const scanResult = document.getElementById("scan-result");

    // Check if scanner already exists and clear previous instance
    if (window.qrScanner) {
        window.qrScanner.clear();
        window.qrScanner = null;
    }

    // Create a new scanner instance
    window.qrScanner = new Html5QrcodeScanner("qr-video", {
        fps: 10,
        qrbox: { width: 250, height: 250 }
    });

    window.qrScanner.render((decodedText) => {
        scanResult.innerText = "Scanned Data: " + decodedText;
        window.qrScanner.clear();
        window.qrScanner = null; // Reset scanner instance

        // Extract ID from the scanned text
        const idMatch = decodedText.match(/ID:\s*(\S+)/);
        const extractedId = idMatch ? idMatch[1] : null;

        if (!extractedId) {
            scanResult.innerText += " ❌ Error: Could not extract ID!";
            return;
        }

        // Send extracted ID to backend for attendance marking
        fetch("http://127.0.0.1:5000/api/mark-attendance", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scanned_id: extractedId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                scanResult.innerText += " ✔ Attendance Marked!";
            } else {
                scanResult.innerText += " ❌ Not Found!";
            }
        })
        .catch(error => {
            console.error("Error:", error);
            scanResult.innerText += " ❌ Error marking attendance!";
        });
    }, (errorMessage) => {
        console.warn("QR Code Scan Error:", errorMessage);
    });
});
