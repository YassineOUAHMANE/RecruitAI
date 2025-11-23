
class FilesInTextDAO():
    def __init__(self,db):
        self.db=db

    def save(self,text_id,file_id):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO files_in_text (text_id,file_id) VALUES (%s,%s)",
            (text_id,file_id)
        )
        self.db.commit()
        return cursor.lastrowid
    