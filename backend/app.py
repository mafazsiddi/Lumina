import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import pickle
import io
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI(title="Plant Scanner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'plant_model.h5')
CLASS_NAMES_PATH = os.path.join(BASE_DIR, 'class_names.pkl')

model_error = None
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(CLASS_NAMES_PATH, 'rb') as f:
        class_names = pickle.load(f)
    print("Model and class names loaded successfully.")
except Exception as e:
    import traceback
    model_error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
    print(f"Error loading model or class names: {model_error}")
    model = None
    class_names = []

def preprocess_image(img_array):
    img = cv2.resize(img_array, (224, 224))
    img = preprocess_input(img)
    return np.expand_dims(img, axis=0)

def get_plant_data(plant_id):
    name = class_names[plant_id] if plant_id < len(class_names) else "Unknown"
    return {
        'common': name,
        'scientific': f"{name} scientificus",
        'description': f"A beautiful {name.lower()} known for its stunning appearance and distinct features.",
        'care': "Water weekly, provide partial sunlight, and use organic fertilizer for optimal growth."
    }

@app.post("/scan")
async def scan_plant(file: UploadFile = File(...)):
    if model is None:
        return {"error": f"Model not loaded properly. Diagnostic details: {model_error}"}
        
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    img_array = np.array(img)
    
    # Original code reads with cv2 (which is BGR)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    processed_img = preprocess_image(img_bgr)
    prediction = model.predict(processed_img)
    plant_id = int(np.argmax(prediction))
    
    plant_data = get_plant_data(plant_id)
    return plant_data

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
