from transformers import ViTImageProcessor, ViTForImageClassification
from PIL import Image
import requests
from omegaconf import OmegaConf
import torch
import io
import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


class PetClassification:
  def __init__(self, config_path):
    self.config = OmegaConf.load(config_path)
    self.model = ViTForImageClassification.from_pretrained(self.config.model_path)
    self.processor = ViTImageProcessor.from_pretrained(self.config.model_path)
  def __call__(self, image: Image.Image):
        """Thực hiện suy luận và trả về nhãn dự đoán"""
        inputs = self.processor(images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits

        predicted_class_idx = logits.argmax(-1).item()
        return self.model.config.id2label[predicted_class_idx]



app = FastAPI()

# Khởi tạo mô hình
pet_classifier = PetClassification("config.yaml")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

## TODO
@app.get('/classify')
async def intro():
    return {
        "system": "Hệ thống nhận diện thú cưng (Chó/Mèo)"
    }

@app.get("/health")
async def health():
    return {"status": "active",
            "model": "google/vit-base-patch16-224"
            }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """Nhận ảnh, xử lý và trả về kết quả JSON"""

    # 1. Kiểm tra định dạng đầu vào (Cơ bản)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Đầu vào là 1 hình ảnh!!")

    try:
        # 2. Đọc dữ liệu ảnh từ buffer
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Dữ liệu ảnh bị trống.")

        image = Image.open(io.BytesIO(content)).convert("RGB")

        # 3. Gọi model từ Class để dự đoán
        label = pet_classifier(image)

        # 4. Trả về kết quả JSON rõ ràng
        return {
            "status": "success",
            "filename": file.filename,
            "prediction": label,
            "message": f"Hệ thống xác nhận đây là: {label}"
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": f"Có lỗi xảy ra: {str(e)}"}
        )
## END TODO

import threading
import uvicorn

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)

thread = threading.Thread(target=run_server, daemon=True)
thread.start()

print("Server started on http://127.0.0.1:8000")