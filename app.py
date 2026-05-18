import os
import requests

print("Scanning for trending AI models...")
try:
    hf_url = "https://huggingface.co"
    response = requests.get(hf_url).json()
    
    if isinstance(response, list) and len(response) > 0:
        top_model = response[0].get('id', "meta-llama/Meta-Llama-3-8B-Instruct")
    elif isinstance(response, dict) and 'recently_trending' in response:
        top_model = response['recently_trending']['repoData']['id']
    else:
        top_model = "meta-llama/Meta-Llama-3-8B-Instruct"
except Exception as e:
    print(f"Error fetching trending list: {e}. Using fallback.")
    top_model = "meta-llama/Meta-Llama-3-8B-Instruct"

model_name = top_model.split('/')[-1]
print(f"Targeting trending model: {top_model}")

api_url = "https://huggingface.co"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

prompt = f"""
Write a complete, production-ready Python code wrapper and setup guide for the AI model '{top_model}'.
Include a clean README.md with developer documentation. Add an ethical developer ad banner markdown placeholder at the top.
"""

print("Generating open-source code wrapper via AI...")
try:
    ai_response = requests.post(api_url, headers=headers, json={"inputs": prompt}).json()
    if isinstance(ai_response, list) and len(ai_response) > 0:
        generated_text = ai_response[0].get('generated_text', '# Error generating documentation')
    elif isinstance(ai_response, dict):
        generated_text = ai_response.get('generated_text', ai_response.get('error', '# Error generating documentation'))
    else:
        generated_text = str(ai_response)
except Exception as e:
    generated_text = f"# Generation Error\nAn error occurred while calling the AI API: {e}"

# FIXED PIPELINE: Ensures absolute path exists before writing
target_dir = os.path.join(os.getcwd(), "packages", model_name)
os.makedirs(target_dir, exist_ok=True)

target_file = os.path.join(target_dir, "README.md")
with open(target_file, "w", encoding="utf-8") as f:
    f.write(f"# {model_name} Python SDK\n\n" + generated_text)

print(f"Successfully generated package assets at {target_file}!")
