import requests
import io
from PIL import Image, ImageDraw

def create_img(text):
    img = Image.new('RGB', (400, 150), color = (255, 255, 255))
    if text:
        d = ImageDraw.Draw(img)
        d.text((10,10), text, fill=(0,0,0))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

URL = "http://127.0.0.1:8000/api/analyze-screenshot"

print("--- Test A: Legitimate recharge ---")
text = "Recharge successful. Rs. 349 for 28 days."
res = requests.post(URL, files={'file': ('test.png', create_img(text), 'image/png')})
print(res.json().get('prediction'))

print("--- Test B: Scam ---")
text = "ACCOUNT SUSPENSION ALERT\nYour account has been temporarily suspended.\nVERIFY YOUR ACCOUNT IMMEDIATELY.\nEnter your username, password and banking details.\nhttp://secure-account-verification.example/login\nFailure to verify within 24 hours will result in permanent closure."
res = requests.post(URL, files={'file': ('test.png', create_img(text), 'image/png')})
print(res.json().get('prediction'))

print("--- Test C: OTP ---")
text = "Your verification code is 482931.\nThis code is valid for 10 minutes.\nDO NOT SHARE this code with anyone."
res = requests.post(URL, files={'file': ('test.png', create_img(text), 'image/png')})
print(res.json().get('prediction'))

print("--- Test D: Blank ---")
res = requests.post(URL, files={'file': ('test.png', create_img(""), 'image/png')})
print(res.json().get('extracted_text'))

print("--- Test E: Invalid ---")
res = requests.post(URL, files={'file': ('test.txt', io.BytesIO(b"Hello"), 'text/plain')})
print(res.status_code, res.json())
