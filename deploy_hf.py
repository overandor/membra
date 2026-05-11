"""Deploy MEMBRA to Hugging Face Spaces."""
import os
from huggingface_hub import HfApi, HfFolder

# Set the token from environment variable
token = os.getenv("HF_TOKEN")
if not token:
    raise ValueError("HF_TOKEN environment variable not set. Please set it with: export HF_TOKEN=your_token")
HfFolder.save_token(token)

api = HfApi()

# Space configuration
space_id = "overandor/membra"  # Change to your username/space-name
space_name = "membra"

# Try to create the space
try:
    print(f"Creating Space: {space_id}")
    api.create_repo(
        repo_id=space_id,
        repo_type="space",
        space_sdk="gradio",
        private=False,
        token=token
    )
    print(f"Space created successfully: https://huggingface.co/spaces/{space_id}")
except Exception as e:
    if "already exists" in str(e).lower() or "already created" in str(e).lower() or "already created this space repo" in str(e).lower():
        print(f"Space already exists: {space_id}")
        print("Proceeding with file upload...")
    else:
        print(f"Space does not exist: {space_id}")
    print("Please create the space manually at: https://huggingface.co/spaces/new")
    print("Choose 'Docker' as SDK and name it 'membra'")
    print("Then run this script again.")

# Files to upload
files_to_upload = [
    "app.py",
    "requirements.txt",
    "README.md",
    ".env.example"
]

# Upload docs directory
if os.path.exists("docs"):
    print("\nUploading docs directory...")
    for root, dirs, files in os.walk("docs"):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, ".")
            try:
                api.upload_file(
                    path_or_fileobj=file_path,
                    path_in_repo=rel_path,
                    repo_id=space_id,
                    repo_type="space",
                    token=token
                )
                print(f"✓ Uploaded: {rel_path}")
            except Exception as e:
                print(f"✗ Failed to upload {rel_path}: {e}")

# Upload files
print("\nUploading files to Space...")
for file in files_to_upload:
    if os.path.exists(file):
        try:
            api.upload_file(
                path_or_fileobj=file,
                path_in_repo=file,
                repo_id=space_id,
                repo_type="space",
                token=token
            )
            print(f"✓ Uploaded: {file}")
        except Exception as e:
            print(f"✗ Failed to upload {file}: {e}")
    else:
        print(f"✗ File not found: {file}")

print("\n✓ Deployment complete!")
print(f"View your Space at: https://huggingface.co/spaces/{space_id}")
