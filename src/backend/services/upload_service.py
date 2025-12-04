from fastapi import File, UploadFile
import random
import string
from const import UPLOAD_DIR 

class UploadService():
    def __init__(self,files_dao):
        self.files_dao=files_dao

    def manage_uploads(self,file: UploadFile = File(...)):
        if not file.filename.lower().endswith(".pdf"):
            return False
        new_name = ''.join(random.choices(string.ascii_letters + string.digits, k=32))+'.pdf'
        with open(f"{UPLOAD_DIR}/{new_name}","wb") as f:
            f.write(file.file.read())
        id=self.files_dao.save(new_name)
        return True
        # ici on doit ajouter la fonction du parser
        # et on doit aussi ajouter le cv dans la base
        # de données vectorielle avec le mem id

    def get_file_path(self,id):
        file=self.files_dao.get(id)
        return f"{UPLOAD_DIR}/{file['filepath']}" if file else None

        
