import os 
from huggingface_hub import snapshot_download
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("HUGGINGFACE_TOKEN")

print("Starting dataset download...")

snapshot_download(
    repo_id = "shrijayan/gov_myscheme",
    repo_type="dataset",
    local_dir="./data/raw",
    token=token
)

print("Dataset downloaded succesfully to data/raw/")
