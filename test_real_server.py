import requests
import io
from PIL import Image, ImageDraw

def create_img(text):
    img = Image.new('RGB', (200, 50), color = (255, 255, 255))
    if text:
        d = ImageDraw.Draw(img)
        d.text((10,10), text, fill=(0,0,0))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

print("Sending request to http://127.0.0.1:8000/api/analyze-screenshot")
try:
    files = {'file': ('test.png', create_img("Account Suspended"), 'image/png')}
    res = requests.post("http://127.0.0.1:8000/api/analyze-screenshot", files=files)
    print("Status:", res.status_code)
    print("Response:", res.text)
except Exception as e:
    print("Error:", e)
