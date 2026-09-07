import sys
sys.path.append('backend')
from main import app
from fastapi.testclient import TestClient
import io
from PIL import Image, ImageDraw

client = TestClient(app)

def create_img(text):
    img = Image.new('RGB', (200, 50), color = (255, 255, 255))
    if text:
        d = ImageDraw.Draw(img)
        d.text((10,10), text, fill=(0,0,0))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def create_invalid():
    return io.BytesIO(b"This is not an image.")

def test():
    results = []

    # Message tests
    r = client.post("/api/analyze-message", json={"message": "Your OTP is 482931. Do not share it."})
    results.append(("Message", "Legitimate OTP", r.status_code, r.json().get('prediction', 'error').upper()))

    r = client.post("/api/analyze-message", json={"message": "Your account has been suspended. Click this link and enter your password."})
    results.append(("Message", "Scam", r.status_code, r.json().get('prediction', 'error').upper()))

    # Email tests
    r = client.post("/api/analyze-email", json={"sender": "test@test.com", "subject": "Hello", "body": "Plain text email."})
    results.append(("Email", "Plain text", r.status_code, "Analysis" if r.status_code==200 else "Error"))

    r = client.post("/api/analyze-email", json={"sender": "test@test.com", "subject": "Hello", "body": "<html><body>HTML email.</body></html>"})
    results.append(("Email", "HTML", r.status_code, "Analysis" if r.status_code==200 else "Error"))

    r = client.post("/api/analyze-email", json={"sender": "test@test.com", "subject": "Promo", "body": "Check this: https://example.com"})
    results.append(("Email", "URL", r.status_code, "Analysis + URL" if len(r.json().get('detected_urls',[]))>0 else "Error"))

    r = client.post("/api/analyze-email", json={"sender": "", "subject": "", "body": ""})
    results.append(("Email", "Empty", r.status_code, "Validation" if r.status_code==400 else "Error"))

    # Screenshot tests
    r = client.post("/api/analyze-screenshot", files={"file": ("test.png", create_img("Valid PNG text"), "image/png")})
    results.append(("Screenshot", "Valid PNG", r.status_code, "Analysis" if r.status_code==200 else "Error"))

    r = client.post("/api/analyze-screenshot", files={"file": ("test.jpg", create_img("Valid JPG text"), "image/jpeg")})
    results.append(("Screenshot", "Valid JPG", r.status_code, "Analysis" if r.status_code==200 else "Error"))

    r = client.post("/api/analyze-screenshot", files={"file": ("blank.png", create_img(""), "image/png")})
    res_pred = r.json().get('prediction') if r.status_code == 200 else ""
    results.append(("Screenshot", "Blank image", r.status_code, "No crash" if r.status_code==200 and res_pred=='safe' else "Error"))

    r = client.post("/api/analyze-screenshot", files={"file": ("test.txt", create_invalid(), "text/plain")})
    results.append(("Screenshot", "Invalid file", r.status_code, "Validation" if r.status_code==415 else "Error"))

    r = client.post("/api/analyze-screenshot", files={"file": ("test.png", create_img("Check this: https://example.com"), "image/png")})
    results.append(("Screenshot", "URL", r.status_code, "Analysis + URL" if len(r.json().get('detected_urls',[]))>0 else "Error"))

    r = client.post("/api/analyze-screenshot", files={"file": ("test.png", create_img("आपका अकाउंट बंद कर दिया गया है। तुरंत सत्यापन करें।"), "image/png")})
    results.append(("Screenshot", "Hindi", r.status_code, "Result" if r.status_code==200 else "Error"))

    r = client.post("/api/analyze-screenshot", files={"file": ("test.png", create_img("Warning: आपका अकाउंट बंद कर दिया गया है।"), "image/png")})
    results.append(("Screenshot", "Mixed language", r.status_code, "Result" if r.status_code==200 else "Error"))

    print("| Feature | Test | HTTP | Result |")
    print("|---|---|---|---|")
    for f, t, s, res in results:
        print(f"| {f} | {t} | {s} | {res} |")

test()
