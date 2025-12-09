
class FilesInTextDAO():
    def __init__(self,db):
        self.db_factory=db

    def save(self,text_id,file_id):
        db = self.db_factory()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO files_in_text (text_id,file_id) VALUES (%s,%s)",
            (text_id,file_id)
        )
        db.commit()
        cursor.close()
        db.close() 
        return cursor.lastrowid
    