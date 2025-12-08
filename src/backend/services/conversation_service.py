from typing import Optional

#pour tester seulement

class ConversationService():
    def __init__(self,conversation_dao,conversation_text_dao,llm_client,file_in_text_dao):
        self.conversation_dao=conversation_dao
        self.conversation_text_dao=conversation_text_dao
        self.file_in_text_dao=file_in_text_dao
        self.llm_client=llm_client
        #pour tester seulement
        # self.mock_llm=LLMClient()
        # self.llm_client=self.mock_llm

    def get_conversation(self,id,offset: Optional[int] = None):
        conversation_time=self.conversation_dao.get(id)
        if not conversation_time:
            return None
        offset=offset if offset else 0
        conversation_content=self.conversation_text_dao.list_by_conversation_id(id,offset=offset)
        for conversation_text in conversation_content:
            if conversation_text["file_ids"]:
                conversation_text["file_ids"]=conversation_text["file_ids"].split(',')
        response={"started_at":conversation_time["started_at"],
                  "updated_at":conversation_time["updated_at"],
                  "offset":offset,
                  "content":conversation_content}
        return response
    
    def process_user_message(self,conversation_id,user_input):
        if not self.conversation_dao.get(conversation_id):
            return None
        response=self.llm_client.call_llm(user_input)
        # ici on doit appeller la fonction du llm
        self.conversation_text_dao.save(conversation_id,user_input,False)
        if not response["text"]:
            return None
        text_id=self.conversation_text_dao.save(conversation_id,response["text"],True)
        for file in response["files"]:
            self.file_in_text_dao.save(text_id,file["file_id"])
        result=self.conversation_text_dao.get_by_text_id(text_id)
        #result["file_ids"]=result["file_ids"].split(",")
        
        file_ids = result.get("file_ids")

        if file_ids:
            result["file_ids"] = file_ids.split(",")
        else:
            result["file_ids"] = []

        return result


    def create_conversation(self,user_input):
        id=self.conversation_dao.save()
        response=self.process_user_message(id,user_input)
        if response:
            return {"id":id,"response":response}
        else:
            return None
    
    def get_all_conversations(self):
        data=self.conversation_dao.find_all()
        return data