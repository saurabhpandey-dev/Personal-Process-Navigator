from google import genai
import os

api_key = os.environ.get("GEMINI_API_KEY")

print("API KEY FOUND:", bool(api_key))

if api_key:
    print("KEY START:", api_key[:5])
    print("KEY LENGTH:", len(api_key))

client = genai.Client(
    api_key=api_key
)

try:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Reply only with: GEMINI WORKING"
    )

    print("\nSUCCESS:")
    print(response.text)

except Exception as e:

    print("\nERROR:")
    print(repr(e))