import os
import uuid
from supabase import create_client, Client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
BUCKET_NAME = "trainer-cvs"


def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL or SUPABASE_SERVICE_KEY/SUPABASE_KEY is missing")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_cv(file_bytes: bytes, filename: str, user_id: int):
    client = get_supabase()
    safe_name = filename.replace(" ", "_")
    path = f"{user_id}/{uuid.uuid4()}_{safe_name}"

    client.storage.from_(BUCKET_NAME).upload(
        path,
        file_bytes,
        {"content-type": "application/pdf", "upsert": False},
    )

    public_url = client.storage.from_(BUCKET_NAME).get_public_url(path)
    return path, public_url


def delete_cv(path: str):
    client = get_supabase()
    if path:
        client.storage.from_(BUCKET_NAME).remove([path])
