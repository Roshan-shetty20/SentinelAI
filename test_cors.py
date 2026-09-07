import requests

url = "http://127.0.0.1:8000/api/analyze-url"
headers = {
    "Origin": "http://127.0.0.1:5500",
    "Access-Control-Request-Method": "POST"
}

res = requests.options(url, headers=headers)
print("OPTIONS Response:", res.status_code)
print("CORS Headers:", res.headers.get("Access-Control-Allow-Origin"))

# Now a POST request
payload = {"url": "http://secure-update-paypal-account.com/login"}
post_headers = {
    "Origin": "http://127.0.0.1:5500"
}
res = requests.post(url, json=payload, headers=post_headers)
print("POST Response:", res.status_code)
print("POST JSON:", res.json())
print("CORS Headers:", res.headers.get("Access-Control-Allow-Origin"))

