
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY not found in .env")
    raise SystemExit(1)

url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{MODEL}:generateContent"
)

headers = {
    "x-goog-api-key": API_KEY,
    "Content-Type": "application/json",
}

payload = {
    "contents": [
        {
            "parts": [
                {"text": "Say hello in one short sentence."}
            ]
        }
    ]
}

try:
    response = httpx.post(
        url,
        headers=headers,
        json=payload,
        timeout=httpx.Timeout(90.0, connect=15.0),
    )

    print("HTTP Status:", response.status_code)

    if response.is_success:
        data = response.json()
        answer = data["candidates"][0]["content"]["parts"][0]["text"]
        print("Gemini response:", answer)
    else:
        print("Gemini error:", response.text[:2000])

except httpx.RequestError as exc:
    print("Connection error:", str(exc))
