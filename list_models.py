import os
import google.genai as genai

API_KEY = os.getenv("GOOGLE_API_KEY", "")
if not API_KEY:
    print("[ERROR] GOOGLE_API_KEY environment variable not set!")
    exit(1)

client = genai.Client(api_key=API_KEY)

try:
    models = client.models.list()
    print("Available Models:")
    print("-" * 70)
    for model in models:
        print(f"  - {model.name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"    Methods: {model.supported_generation_methods}")
except Exception as e:
    print(f"Error listing models: {e}")
    import traceback
    traceback.print_exc()
