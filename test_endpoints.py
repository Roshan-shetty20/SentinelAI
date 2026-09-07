import sys
sys.path.append('backend')
from main import app, EmailRequest, analyze_email, analyze_screenshot, MessageRequest
from fastapi.testclient import TestClient
import asyncio

client = TestClient(app)

def test():
    print("--- Test Email ---")
    res = client.post("/api/analyze-email", json={"sender": "test@example.com", "subject": "Alert", "body": "Your account is suspended."})
    print(res.status_code)
    print(res.json())

    print("--- Test Screenshot ---")
    # create a dummy image
    from PIL import Image
    import io
    img = Image.new('RGB', (100, 30), color = (73, 109, 137))
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(img)
    d.text((10,10), "Account Suspended", fill=(255,255,0))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    res = client.post("/api/analyze-screenshot", files={"file": ("test.png", img_byte_arr, "image/png")})
    print(res.status_code)
    print(res.json())

test()
