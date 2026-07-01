import numpy as np
import pickle
import io
from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
import h5py
import torch
import torch.nn as nn
from torchvision import models, transforms

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

# Define PyTorch model structure matching the saved state dict
class PlantModel(nn.Module):
    def __init__(self, num_classes=47):
        super().__init__()
        # Load the base MobileNetV2 architecture
        self.base_model = models.mobilenet_v2(weights=None)
        # Reconstruct the custom classifier head to match the state dict:
        # classifier.0: Linear(1280 -> 1024)
        # classifier.1: ReLU
        # classifier.2: Dropout(p=0.2)
        # classifier.3: Linear(1024 -> 47)
        self.base_model.classifier = nn.Sequential(
            nn.Linear(1280, 1024),
            nn.ReLU(),
            nn.Dropout(p=0.2),
            nn.Linear(1024, num_classes)
        )
        
    def forward(self, x):
        return self.base_model(x)

# Preprocessing transforms (Resize, CenterCrop, Normalize)
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

model = None
class_names = []
model_error = None

try:
    # 1. Load class names
    with open(CLASS_NAMES_PATH, 'rb') as f:
        class_names = pickle.load(f)
    num_classes = len(class_names) if class_names else 47
    
    # 2. Instantiate PyTorch model
    model = PlantModel(num_classes=num_classes)
    
    # 3. Load state dict from HDF5 file
    model_state_dict = model.state_dict()
    state_dict = {}
    with h5py.File(MODEL_PATH, 'r') as f:
        for key in model_state_dict.keys():
            if key in f:
                state_dict[key] = torch.from_numpy(np.array(f[key]))
            else:
                print(f"Warning: Key {key} not found in model file.")
            
    model.load_state_dict(state_dict, strict=False)
    model.eval()  # Set to evaluation mode
    print("PyTorch model and class names loaded successfully.")
except Exception as e:
    import traceback
    model_error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
    print(f"Error loading model or class names: {model_error}")
    model = None
    class_names = []

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
        
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Apply preprocessing
        input_tensor = preprocess(img)
        input_batch = input_tensor.unsqueeze(0)  # Add batch dimension
        
        # Run inference
        with torch.no_grad():
            output = model(input_batch)
            prediction = torch.argmax(output, dim=1).item()
            
        plant_data = get_plant_data(prediction)
        return plant_data
    except Exception as e:
        return {"error": f"Inference failed: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
