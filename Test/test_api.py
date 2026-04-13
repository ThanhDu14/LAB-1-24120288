import requests
import io

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    print("\n--- Testing GET /classify ---")
    try:
        response = requests.get(f"{BASE_URL}/classify")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Lỗi khi gọi /: {e}")

def test_health():
    print("\n--- Testing GET /health ---")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Lỗi khi gọi /health: {e}")

def test_predict():
    print("\n--- Testing POST /predict ---")
    img_url = "https://sieupet.com/sites/default/files/pictures/images/cho-pug-bieu-cam.jpg"
    try:
        img_data = requests.get(img_url).content
        
        files = {'file': ('pug.jpg', io.BytesIO(img_data), 'image/jpeg')}
        
        response = requests.post(f"{BASE_URL}/predict", files=files)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Lỗi khi gọi /predict: {e}")

if __name__ == "__main__":
    test_root()
    test_health()
    test_predict()
    print("\n--- Hoàn thành kiểm thử ---")