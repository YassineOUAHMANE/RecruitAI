from fastapi import APIRouter,Query,Request
from typing import Optional

class ConversationController():
    def __init__(self,conversation_service):
        self.conversation_service=conversation_service
        self.router_api=APIRouter()
        self.router_api.add_api_route("/conversation/{id}",self.load_conversation,methods=["GET"])
        self.router_api.add_api_route("/conversation/{id}",self.send_message_to_ai,methods=["POST"])
        self.router_api.add_api_route("/conversation/",self.create_conversation,methods=["PUT"])
        self.router_api.add_api_route("/conversation/from-file",self.create_from_file,methods=["POST"])
        self.router_api.add_api_route("/conversation/",self.load_all,methods=["GET"])
 

    def load_conversation(self,id:int,offset: Optional[int] = Query(None, ge=0)):
        content=self.conversation_service.get_conversation(id)
        return {"message":content if content else "loading conversation failed"}
    
    async def send_message_to_ai(self,id:int,request: Request):
        data=await request.json()
        ai_response=self.conversation_service.process_user_message(id,data["text"])
        return {"message":ai_response if ai_response else "failed to generate AI response"}
    
    async def create_conversation(self,request: Request):
        data=await request.json()
        ai_response=self.conversation_service.create_conversation(data["text"])
        return {"message":ai_response if ai_response else "failed to generate AI response"}
    
    async def create_from_file(self,request: Request):
        data=await request.json()
        file_id=data.get("file_id")
        prompt=data.get("prompt", "Analyze this CV")
        result=self.conversation_service.create_conversation_from_file(file_id, prompt)
        return {"message":result if result else "failed to create conversation from file"}
    
    def load_all(self):
        data=self.conversation_service.get_all_conversations()
        return {"message":data}





    