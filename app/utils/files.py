import shutil
import tempfile
from fastapi import File, UploadFile


def get_upload_file_path(file: UploadFile = File(...)) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
        return tmp_path
