import os
import requests

print("Initializing AI Factory Engine...")

# Stable target model for development
top_model = "meta-llama/Meta-Llama-3-8B-Instruct"
model_name = "Meta-Llama-3-SDK"

print(f"Targeting model architecture: {top_model}")

# Hugging Face Serverless Inference Gateway 
api_url = f"https://huggingface.co{top_model}"
headers = {
    "Authorization": f"Bearer {os.getenv('HF_TOKEN')}",
    "Content-Type": "application/json"
}

prompt = f"""
Generate a comprehensive, production-ready Python SDK integration wrapper and installation guide for the AI model '{top_model}'.
Provide a complete README.md outline. Include an ethical developer ad banner markdown placeholder at the very top of the document.
"""

print("Requesting assets from Hugging Face API layer...")
generated_text = ""

try:
    response = requests.post(api_url, headers=headers, json={"inputs": prompt, "parameters": {"max_new_tokens": 800}}, timeout=45)
    res_data = response.json()
    
    if isinstance(res_data, list) and len(res_data) > 0:
        generated_text = res_data[0].get('generated_text', '')
    elif isinstance(res_data, dict):
        generated_text = res_data.get('generated_text', res_data.get('error', ''))
except Exception as e:
    print(f"API connection warning: {e}")

# Fallback template formatting if API is loading or busy
if not generated_text or "loading" in str(generated_text).lower() or len(generated_text) < 100:
    print("API is initializing. Deploying clean structural documentation framework.")
    generated_text = f"""# {model_name} Universal Python Wrapper

[![Developer Ad Banner](https://shields.io)](https://ethicalads.io)

An automated client integration layer optimized for querying the underlying `{top_model}` architecture natively.

## Installation
```bash
pip install universal-ai-bridges
```

## Quickstart
```python
import requests

def query_model(prompt, token):
    api_url = "https://huggingface.co{top_model}"
    headers = {{"Authorization": f"Bearer {{token}}"}}
    response = requests.post(api_url, headers=headers, json={{"inputs": prompt}})
    return response.json()
```
"""

# Save folder paths
target_dir = os.path.join(os.getcwd(), "packages", model_name)
os.makedirs(target_dir, exist_ok=True)

target_file = os.path.join(target_dir, "README.md")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(generated_text)

print(f"Asset pipeline successfully written to: {target_file}")
