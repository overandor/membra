"""Deploy overworker to Hugging Face Spaces."""
import os
from huggingface_hub import HfApi, HfFolder

token = os.getenv("HF_TOKEN")
if not token:
    raise ValueError("HF_TOKEN environment variable not set")
HfFolder.save_token(token)

api = HfApi()
space_id = "luguog/overworker"

try:
    print(f"Creating Space: {space_id}")
    api.create_repo(
        repo_id=space_id,
        repo_type="space",
        space_sdk="gradio",
        private=False,
        token=token
    )
    print(f"Space created: https://huggingface.co/spaces/{space_id}")
except Exception as e:
    if "already exists" in str(e).lower():
        print(f"Space already exists: {space_id}")
    else:
        print(f"Error: {e}")
        exit(1)

all_files = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'node_modules', '.pytest_cache']]
    for file in files:
        if file.endswith(('.py', '.txt', '.md', '.html', '.json', '.yaml')):
            file_path = os.path.join(root, file)
            if file_path.startswith('./'):
                file_path = file_path[2:]
            all_files.append(file_path)

print(f"\nUploading {len(all_files)} files to Space...")
for file_path in all_files:
    if file_path == "deploy_hf.py":
        continue
    if os.path.exists(file_path):
        try:
            api.upload_file(
                path_or_fileobj=file_path,
                path_in_repo=file_path,
                repo_id=space_id,
                repo_type="space",
                token=token
            )
            print(f"Uploaded: {file_path}")
        except Exception as e:
            print(f"Failed {file_path}: {e}")

print(f"\nDeployment complete: https://huggingface.co/spaces/{space_id}")
