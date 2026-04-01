import requests
import io

API_URL = "http://xfmlf-34-12-239-76.a.free.pinggy.link/predict"

img_url = "https://sieupet.com/sites/default/files/pictures/images/cho-pug-bieu-cam.jpg"

img_data = requests.get(img_url).content

files = {'file': ('pug.jpg', io.BytesIO(img_data), 'image/jpeg')}

response = requests.post(API_URL, files=files)

print(response.json())