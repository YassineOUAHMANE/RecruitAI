from fastapi import APIRouter, File, UploadFile,Query
from starlette.responses import FileResponse

class UploadController():
    def __init__(self,upload_service):
        self.upload_service=upload_service
        self.router_api=APIRouter()
        self.router_api.add_api_route("/upload",self.upload_user_cv,methods=["POST"])
        self.router_api.add_api_route("/files/{file_id}",self.get_file_content,methods=["GET"])


    def upload_user_cv(self,file: UploadFile = File(...)):
        result = self.upload_service.manage_uploads(file)
        if result["success"]:
            return {"message":"success", "file_id": result["file_id"]}
        else:
            return {"message":"upload failed", "file_id": None}
    
    def get_file_content(self,file_id):
        filepath=self.upload_service.get_file_path(file_id)
        return FileResponse(filepath) if filepath else {"message":"failed to get file content"}

    
