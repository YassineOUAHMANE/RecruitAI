from fastapi import APIRouter, File, UploadFile,Query,FileResponse

class UploadController():
    def __init__(self,upload_service):
        self.upload_service=upload_service
        self.router_api=APIRouter()
        self.router_api.add_api_route("/upload",self.upload_user_cv,methods=["POST"])
        self.router_api.add_api_route("/files/{file_id}",self.get_file_content,methods=["GET"])


    def upload_user_cv(self,file: UploadFile = File(...)):
        success=self.upload_service.manage_uploads(file)
        return {"message":"success" if success else "upload failed"}
    
    def get_file_content(self,file_id):
        filepath=self.upload_service.get_file_path(file_id)
        return FileResponse(filepath) if filepath else {"message":"failed to get file content"}

    
