
class ConversationDAO():
    def __init__(self,db):
        self.db=db

    def get(self,id):
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(
            "SELECT started_at,updated_at FROM conversations WHERE id=%s",
            (id,)
        )
        row = cursor.fetchone()
        return row
    
    def save(self):
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO conversations () VALUES ()",
            ()
        )
        self.db.commit()
        return cursor.lastrowid
    
