import requests
import json

def llama_call(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
    )

    result = response.json()
    return result["response"]   