# main.py
import cv2
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import pickle

class PlantScannerApp:
    def __init__(self):
        self.model = tf.keras.models.load_model('plant_model.h5')
        with open('class_names.pkl', 'rb') as f:
            self.class_names = pickle.load(f)
        
        self.setup_ui()
        self.cap = cv2.VideoCapture(0)
        self.update_camera()

    def setup_ui(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        self.root = ctk.CTk()
        self.root.title("Plant Scanner")
        self.root.geometry("800x600")
        
        # Camera Preview
        self.camera_label = ctk.CTkLabel(self.root, text="")
        self.camera_label.pack(pady=20)
        
        # Scan Button
        self.scan_button = ctk.CTkButton(
            self.root,
            text="SCAN PLANT",
            command=self.scan_plant,
            corner_radius=32,
            fg_color="#2E8B57",
            hover_color="#3CB371",
            height=50,
            width=200
        )
        self.scan_button.pack(pady=10)
        
        # Results Frame
        self.results_frame = ctk.CTkFrame(self.root)
        self.results_frame.pack(pady=20, fill='both', expand=True, padx=20)
        
        self.result_labels = {
            'name': ctk.CTkLabel(self.results_frame, text="Plant Name: ", font=("Arial", 18)),
            'scientific': ctk.CTkLabel(self.results_frame, text="Scientific Name: ", font=("Arial", 14)),
            'description': ctk.CTkLabel(self.results_frame, text="Description: ", wraplength=600),
            'care': ctk.CTkLabel(self.results_frame, text="Care Tips: ", wraplength=600)
        }
        
        for label in self.result_labels.values():
            label.pack(pady=5, anchor='w')

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.camera_label.configure(image=imgtk)
            self.camera_label.image = imgtk
        self.root.after(10, self.update_camera)

    def scan_plant(self):
        ret, frame = self.cap.read()
        if ret:
            processed_img = self.preprocess_image(frame)
            prediction = self.model.predict(processed_img)
            plant_id = np.argmax(prediction)
            self.display_results(plant_id)

    def preprocess_image(self, img):
        img = cv2.resize(img, (224, 224))
        img = preprocess_input(img)
        return np.expand_dims(img, axis=0)

    def display_results(self, plant_id):
        plant_data = self.get_plant_data(plant_id)
        self.result_labels['name'].configure(text=f"Plant Name: {plant_data['common']}")
        self.result_labels['scientific'].configure(text=f"Scientific Name: {plant_data['scientific']}")
        self.result_labels['description'].configure(text=f"Description: {plant_data['description']}")
        self.result_labels['care'].configure(text=f"Care Tips: {plant_data['care']}")

    def get_plant_data(self, plant_id):
        # Replace with your actual database
        return {
            'common': self.class_names[plant_id],
            'scientific': "Scientificius plantus",
            'description': "A beautiful flowering plant with medicinal properties...",
            'care': "Water weekly, partial sunlight, use organic fertilizer..."
        }

    def run(self):
        self.root.mainloop()
        self.cap.release()

if __name__ == "__main__":
    app = PlantScannerApp()
    app.run()