# Lumina - AI Plant Scanner 🌿✨

Lumina is a premium, minimalist web application that uses Artificial Intelligence to identify plants in real-time through your device's camera. 

Built with a stunning glassmorphism interface and powered by a robust machine learning backend, Lumina seamlessly blends beautiful design with powerful computer vision.

## ✨ Features
* **Real-time Camera Feed:** Directly access your device's camera securely from the browser.
* **Instant AI Inference:** Powered by TensorFlow and MobileNetV2 for lightning-fast plant classification.
* **Premium UI/UX:** A stunning dark-mode interface featuring glassmorphism, fluid animations, and a handcrafted SVG vector logo.
* **Decoupled Architecture:** Clean separation between the Vanilla JS frontend and the Python API.

## 🚀 Tech Stack
* **Frontend:** HTML5, Vanilla JavaScript, CSS3 (Glassmorphism & CSS Animations)
* **Backend:** Python, FastAPI, Uvicorn
* **Machine Learning:** TensorFlow, OpenCV, Numpy

## 💻 Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/plant-scanner.git
   cd plant-scanner
   ```

2. Run the application (Windows):
   Simply double click the `run.bat` file! This will automatically install dependencies and start both the frontend and backend servers.
   
   *Alternatively, run manually:*
   ```bash
   pip install -r requirements.txt
   cd backend && uvicorn app:app --host 127.0.0.1 --port 8000
   cd frontend && python -m http.server 8080
   ```

3. Open your browser and navigate to `http://127.0.0.1:8080`.

## ☁️ Cloud Deployment

* **Frontend:** Designed to be easily hosted on platforms like **Netlify** or Vercel. Just deploy the `/frontend` directory!
* **Backend:** Ready for **Render**, Heroku, or Railway. (Uses `opencv-python-headless` for headless server compatibility).
