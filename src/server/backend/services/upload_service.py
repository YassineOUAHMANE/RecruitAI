from fastapi import File, UploadFile
import random
import string
from backend.const import UPLOAD_DIR 

class UploadService():
    def __init__(self,files_dao,ingestor):
        self.files_dao=files_dao
        self.ingestor = ingestor
    def manage_uploads(self,file: UploadFile = File(...)):
        if not file.filename.lower().endswith(".pdf"):
            return {"success": False, "file_id": None}
        new_name = ''.join(random.choices(string.ascii_letters + string.digits, k=32))+'.pdf'
        full_path=f"{UPLOAD_DIR}/{new_name}"
        with open(full_path,"wb") as f:
            f.write(file.file.read())
        file_id=self.files_dao.save(full_path)
        self.ingestor.ingest_one(file_id, full_path)
        return {"success": True, "file_id": file_id}

    def get_file_path(self,id):
        file=self.files_dao.get(id)
        return file['filepath'] if file else None

        
