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
            return False
        new_name = ''.join(random.choices(string.ascii_letters + string.digits, k=32))+'.pdf'
        full_path=f"{UPLOAD_DIR}/{new_name}"
        with open(full_path,"wb") as f:
            f.write(file.file.read())
        id=self.files_dao.save(full_path)
        self.ingestor.ingest_one(id, full_path)
        return True
        # ici on doit ajouter la fonction du parser
        # et on doit aussi ajouter le cv dans la base
        # de données vectorielle avec le mem id

    def get_file_path(self,id):
        file=self.files_dao.get(id)
        return file['filepath'] if file else None

        
