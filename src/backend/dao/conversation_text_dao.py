
class ConversationTextDAO():
    def __init__(self,db):
        self.db_factory=db

    def save(self,conversation_id,text,sent_by_AI):
        db=self.db_factory()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO conversation_text (sent_by_AI,text,conversation_id) VALUES (%s,%s,%s)",
            (sent_by_AI,text,conversation_id)
        )
        db.commit()
        cursor.close()
        db.close() 
        return cursor.lastrowid
    def list_by_conversation_id(self,conversation_id,offset=0,limit=10):
        limit=int(limit)
        offset=int(offset)
        db=self.db_factory()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            f"""
            SELECT 
                ct.id, 
                ct.sent_at, 
                ct.sent_by_AI, 
                ct.text,
                GROUP_CONCAT(fit.file_id) AS file_ids
            FROM conversation_text ct
            LEFT JOIN files_in_text fit ON fit.text_id = ct.id
            WHERE ct.conversation_id=%s
            GROUP BY ct.id
            ORDER BY ct.id DESC
            LIMIT {limit} OFFSET {offset}
            """,
            (conversation_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        db.close() 
        return rows
    
    def get_by_text_id(self,text_id):
        db=self.db_factory()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            f"""
            SELECT 
                ct.id, 
                ct.sent_at, 
                ct.sent_by_AI, 
                ct.text,
                GROUP_CONCAT(fit.file_id) AS file_ids
            FROM conversation_text ct
            LEFT JOIN files_in_text fit ON fit.text_id = ct.id
            WHERE ct.id=%s
            GROUP BY ct.id
            """,
            (text_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        db.close() 
        return row
    