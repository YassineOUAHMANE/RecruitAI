
class ConversationDAO():
    def __init__(self,db):
        self.db_factory=db

    def get(self,id):
        db=self.db_factory()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT started_at,updated_at FROM conversations WHERE id=%s",
            (id,)
        )
        row = cursor.fetchone()
        cursor.close()
        db.close() 
        return row
    
    def save(self):
        db=self.db_factory()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO conversations () VALUES ()",
            ()
        )
        db.commit()
        return cursor.lastrowid
    
    def find_all(self):
        db=self.db_factory()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, started_at, updated_at FROM conversations"
        )
        rows = cursor.fetchall()
        cursor.close()
        db.close() 
        return rows
    
