
class FilesDAO():
    def __init__(self,db):
        self.db_factory=db

    def save(self,filepath):
        db=self.db_factory()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO files (filepath) VALUES (%s)",
            (filepath,)
        )
        db.commit()
        cursor.close()
        db.close() 
        return cursor.lastrowid
    
    def get(self,id):
        db=self.db_factory()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT filepath FROM files WHERE id=%s",
            (id,)
        )
        row = cursor.fetchone()
        cursor.close()
        db.close() 
        return row
