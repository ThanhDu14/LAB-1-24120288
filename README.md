# Pet Classification System

## Thông tin sinh viên
- **Họ và tên:** Nguyễn Thành Dự 
- **Mã số sinh viên:** 24120288
- **Lớp / Khóa:** 24CTT3

## Tên mô hình và liên kết HF
- **Tên mô hình:** Google ViT (Vision Transformer) Base Patch 16 (224x224)
- **Liên kết Hugging Face:** [google/vit-base-patch16-224](https://huggingface.co/google/vit-base-patch16-224)

## Mô tả ngắn về chức năng của hệ thống
Hệ thống cung cấp một API nhận diện hình ảnh động vật (như chó, mèo, v.v.) dựa trên kiến trúc mô hình học sâu Vision Transformer (ViT). 
Người dùng có thể tải lên một bức ảnh thú cưng qua hệ thống API, máy chủ sẽ tiến hành trích xuất đặc trưng hình ảnh và trả về nhãn dự đoán tương ứng với độ chính xác cao dựa trên mô hình `vit-base-patch16-224` đã được tinh chỉnh trên ImageNet.

## Hướng dẫn cài đặt thư viện
Yêu cầu máy tính đã cài đặt sẵn Python. Để cài đặt các thư viện cần thiết (có thể tạo môi trường ảo ảo `venv` hoặc `conda` trước khi cài), hãy chạy lệnh sau trong terminal tại thư mục gốc của project:

```bash
pip install -r requirements.txt
```

## Hướng dẫn chạy chương trình
1. Mở terminal tại thư mục gốc của project.
2. Khởi chạy server FastAPI bằng lệnh `uvicorn`:
```bash
uvicorn App.main:app --host 127.0.0.1 --port 8000 --reload
```
3. Sau khi chạy lệnh này, server sẽ bắt đầu lắng nghe tại địa chỉ `http://127.0.0.1:8000`.

## Hướng dẫn gọi API và ví dụ request/response

Hệ thống có 3 API Endpoint chính:

### 1. `GET /classify`
- **Chức năng:** Trả về thông tin giới thiệu chung của hệ thống.
- **Request mẫu (cURL):**
  ```bash
  curl -X GET "http://127.0.0.1:8000/classify"
  ```
- **Response mẫu:**
  ```json
  {
      "system": "Hệ thống nhận diện thú cưng (Chó/Mèo)"
  }
  ```

### 2. `GET /health`
- **Chức năng:** Kiểm tra trạng thái hoạt động của server và cấu hình mô hình đang sử dụng.
- **Request mẫu (cURL):**
  ```bash
  curl -X GET "http://127.0.0.1:8000/health"
  ```
- **Response mẫu:**
  ```json
  {
      "status": "active",
      "model": "google/vit-base-patch16-224"
  }
  ```

### 3. `POST /predict`
- **Chức năng:** Nhận một tệp tin hình ảnh tải lên, xử lý phân loại ảnh qua mô hình và trả về kết quả dự đoán nhãn của vật nuôi.
- **Tham số:** `file` (form-data) - Tệp tin hình ảnh (chấp nhận các định dạng ảnh hợp lệ bắt đầu bằng `image/`).
- **Request mẫu sử dụng Python API (`requests`):**
  ```python
  import requests

  url = "http://127.0.0.1:8000/predict"
  files = {'file': ('cho-pug.jpg', open('path_to_image/cho-pug.jpg', 'rb'), 'image/jpeg')}
  response = requests.post(url, files=files)
  
  print(response.json())
  ```
- **Request mẫu sử dụng cURL:**
  ```bash
  curl -X POST "http://127.0.0.1:8000/predict" \
       -H "accept: application/json" \
       -H "Content-Type: multipart/form-data" \
       -F "file=@path_to_image/cho-pug.jpg"
  ```
- **Response mẫu (Thành công):**
  ```json
  {
      "status": "success",
      "filename": "cho-pug.jpg",
      "prediction": "pug, pug-dog",
      "message": "Hệ thống xác nhận đây là: pug, pug-dog"
  }
  ```


## Liên kết video demo
- **Video Demo:**
