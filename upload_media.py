import os
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

MEDIA_DIR = Path("media")
BUCKET = "media"

if not MEDIA_DIR.exists():
    print("❌ media folder not found!")
    exit()

uploaded = 0
failed = 0
import mimetypes

def get_content_type(file_path):
    content_type, _ = mimetypes.guess_type(file_path)
    return content_type or "application/octet-stream"
for file_path in MEDIA_DIR.rglob("*"):
    if not file_path.is_file():
        continue

    # Convert Windows path to Supabase storage path
    storage_path = file_path.relative_to(MEDIA_DIR).as_posix()

    try:
        with open(file_path, "rb") as f:
            file_data = f.read()

        # Upload
        supabase.storage.from_(BUCKET).upload(
            storage_path,
            file_data,
            {
                "upsert": "true",
                "content-type": get_content_type(file_path)
            }
        )

        print(f"✅ Uploaded: {storage_path}")
        uploaded += 1

    except Exception as e:
        print(f"❌ Failed: {storage_path}")
        print(e)
        failed += 1

print("\n----------------------------")
print(f"Uploaded: {uploaded}")
print(f"Failed:   {failed}")
print("----------------------------")