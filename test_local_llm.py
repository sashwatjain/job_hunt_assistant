import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "mistral",
        "prompt": "Say hello in one line",
        "stream": False
    }
)

print("Status:", response.status_code)
print("Body:", response.text)