document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('camera-feed');
    const scanBtn = document.getElementById('scan-btn');
    const btnText = scanBtn.querySelector('.btn-text');
    const btnLoader = scanBtn.querySelector('.btn-loader');
    const scanOverlay = document.getElementById('scan-overlay');
    const resultsCard = document.getElementById('results-card');
    const closeBtn = document.getElementById('close-btn');

    // DOM Elements for results
    const plantNameEl = document.getElementById('plant-name');
    const scientificNameEl = document.getElementById('scientific-name');
    const plantDescriptionEl = document.getElementById('plant-description');
    const plantCareEl = document.getElementById('plant-care');

    // Initialize Camera
    async function initCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: { facingMode: 'environment' }
            });
            video.srcObject = stream;
        } catch (err) {
            console.error('Error accessing camera:', err);
            alert('Unable to access the camera. Please ensure you have granted permissions.');
        }
    }

    // Capture frame from video
    function captureFrame() {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        return new Promise(resolve => {
            canvas.toBlob(blob => resolve(blob), 'image/jpeg', 0.9);
        });
    }

    // Handle Scan
    async function scanPlant() {
        // UI Loading State
        scanBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline-block';
        scanOverlay.classList.add('active');
        resultsCard.classList.remove('show');

        try {
            const imageBlob = await captureFrame();
            
            const formData = new FormData();
            formData.append('file', imageBlob, 'capture.jpg');

            const response = await fetch('https://lumina-4cu9.onrender.com/scan', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            if (data.error) {
                alert('Error: ' + data.error);
                return;
            }

            // Populate Results
            plantNameEl.textContent = data.common;
            scientificNameEl.textContent = data.scientific;
            plantDescriptionEl.textContent = data.description;
            plantCareEl.textContent = data.care;

            // Show Results Card
            resultsCard.classList.add('show');

        } catch (error) {
            console.error('Scanning error:', error);
            alert('Error scanning the plant. Make sure the backend server is running.');
        } finally {
            // Reset UI
            scanBtn.disabled = false;
            btnText.style.display = 'inline-block';
            btnLoader.style.display = 'none';
            scanOverlay.classList.remove('active');
        }
    }

    // Event Listeners
    scanBtn.addEventListener('click', scanPlant);
    
    closeBtn.addEventListener('click', () => {
        resultsCard.classList.remove('show');
    });

    // Start
    initCamera();
});
