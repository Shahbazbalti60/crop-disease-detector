from ultralytics import YOLO
from PIL import Image

model = None

def load_model(model_path="model/best.pt"):
    global model
    if model is None:
        model = YOLO(model_path)
    return model

def predict(image: Image.Image, model_path="model/best.pt"):
    m = load_model(model_path)
    results = m(image)
    
    top1_idx = results[0].probs.top1
    top1_conf = results[0].probs.top1conf.item()
    class_name = results[0].names[top1_idx]
    
    # Clean up class name
    # e.g. "Tomato___Early_blight" → crop: Tomato, disease: Early blight
    parts = class_name.split("___")
    crop = parts[0].replace("_", " ")
    disease = parts[1].replace("_", " ") if len(parts) > 1 else "Unknown"
    
    return {
        "class_name": class_name,
        "crop": crop,
        "disease": disease,
        "confidence": round(top1_conf * 100, 2)
    }