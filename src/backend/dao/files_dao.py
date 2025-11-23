
class FilesDAO():
    def __init__(self,db):
        self.db=db

    def save(self,filepath):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO files (filepath) VALUES (%s)",
            (filepath,)
        )
        self.db.commit()
        return cursor.lastrowid
    
    def get(self,id):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(
            "SELECT filepath FROM files WHERE id=%s",
            (id,)
        )
        row = cursor.fetchone()
        return row
