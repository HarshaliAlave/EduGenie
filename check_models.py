from google import genai

# Replace with your key
API_KEY = "AIzaSyDcb25h4AD7LRHkcTnlF_N3ap00g2ETMsc"

client = genai.Client(api_key=API_KEY)

print("Available models:")
for model in client.models.list():
    print("-", model.name)