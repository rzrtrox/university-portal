import os

from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()


class SupabaseStorage(Storage):

    def __init__(self):
        self.supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_SERVICE_KEY"),
        )
        self.bucket = "media"

    def _save(self, name, content):
        file_data = content.read()

        # Upload / replace file
        self.supabase.storage.from_(self.bucket).upload(
            name,
            file_data,
            {
                "upsert": "true",
            }
        )

        return name

    def _open(self, name, mode="rb"):
        response = self.supabase.storage.from_(self.bucket).download(name)

        return ContentFile(response)

    def delete(self, name):
        self.supabase.storage.from_(self.bucket).remove([name])

    def exists(self, name):
        try:
            self.supabase.storage.from_(self.bucket).download(name)
            return True
        except Exception:
            return False

    def url(self, name):
        return (
            f"{os.getenv('SUPABASE_URL')}"
            f"/storage/v1/object/public/{self.bucket}/{name}"
        )