# test_ollama.py
import requests

r = requests.post(
    "http://127.0.0.1:11434/api/generate",
    json={
        "model": "tinyllama",
        "prompt": "Say hello in JSON only",
        "stream": False
    }
)

print(r.json())
