from fastapi import UploadFile, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import uuid
from pathlib import Path

load_dotenv()

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "photography")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


SAVE_DIRECTORY = "images"
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".bmp"}

# Crear carpeta local para guardar temporalmente
parent_path = os.path.dirname(os.getcwd())
save_path = os.path.join(parent_path, SAVE_DIRECTORY)
os.makedirs(save_path, exist_ok=True)

async def upload_img_supabase(upload_file: UploadFile, subfolder: str = "photographers") -> str:
    file_ext = Path(upload_file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXT:
        raise HTTPException(status_code=400, detail="Tipo de archivo no permitido")

    if subfolder not in {"photographers", "photos"}:
        raise HTTPException(status_code=400, detail="Subcarpeta inválida")

    file_name = f"{subfolder}/{uuid.uuid4().hex[:8]}_{upload_file.filename}"
    contents = await upload_file.read()

    response = supabase.storage.from_(SUPABASE_BUCKET).upload(
        file_name, contents, {"content-type": upload_file.content_type}
    )

    print("DEBUG response:", response)

    public_url = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{file_name}"
    return public_url
