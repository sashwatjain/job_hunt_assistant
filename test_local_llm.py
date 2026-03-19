import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": "Say hello in one line",
        "stream": False
    }
)

print(response.json()["response"])