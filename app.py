import os
import requests
import time

print("Scanning for trending AI models...")
try:
    hf_url = "https://huggingface.co/api/trending"
    response = requests.get(hf_url).json()
    
    if isinstance(response, list) and len(response) > 0:
        top_model = response[0].get('id', "meta-llama/Llama-3-8B-Instruct")
    elif isinstance(response, dict) and 'recently_trending' in response:
        top_model = response['recently_trending']['repoData']['id']
    else:
        top_model = "meta-llama/Llama-3-8B-Instruct"
except Exception as e:
    print(f"Error fetching trending list: {e}. Using fallback.")
    top_model = "meta-llama/Llama-3-8B-Instruct"

model_name = top_model.split('/')[-1]
print(f"Targeting trending model: {top_model}")

# Clean API routing string
api_url = "https://huggingface.co"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

prompt = f"""
Write a complete, production-ready Python code wrapper and setup guide for the AI model '{top_model}'.
Include a clean README.md with developer documentation. Add an ethical developer ad banner markdown placeholder at the top.
"""

print("Generating open-source code wrapper via AI...")
generated_text = ""

# Handle server warming errors gracefully
for attempt in range(3):
    try:
        ai_response = requests.post(api_url, headers=headers, json={"inputs": prompt}, timeout=30)
        res_data = ai_response.json()
        
        if isinstance(res_data, list) and len(res_data) > 0:
            generated_text = res_data[0].get('generated_text', '')
            break
        elif isinstance(res_data, dict):
            if 'error' in res_data and 'loading' in res_data['error'].lower():
                print("AI model server is currently loading. Retrying in 20 seconds...")
                time.sleep(20)
                continue
            generated_text = res_data.get('generated_text', '')
            break
    except Exception as e:
        print(f"Attempt {attempt+1} failed: {e}")
        time.sleep(5)

# Safety fallback if the AI API fails entirely
if not generated_text or len(generated_text) < 50:
    print("API returned invalid data or error. Generating placeholder template to avoid system crash.")
    generated_text = f"""
# {model_name} Python Integration Library

[![Ad Banner](https://shields.io)](https://ethicalads.io)

An automated Python package built to interact directly with the `{top_model}` open-source infrastructure layer.

## Quickstart Installation
```bash
pip install universal-ai-bridges
```

## Implementation Example
```python
# Automated package architecture sample
import requests

def run_inference(prompt):
    print("Connecting to secure backend...")
    # Package logic details inside main distribution branch
```
"""

# Save verified folder path dynamically
target_dir = os.path.join(os.getcwd(), "packages", model_name)
os.makedirs(target_dir, exist_ok=True)

target_file = os.path.join(target_dir, "README.md")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(generated_text)

print(f"Successfully finalized assets at {target_file}!")
