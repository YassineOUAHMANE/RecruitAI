from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
import os

from backend.dao.conversations_dao import ConversationDAO
from backend.dao.conversation_text_dao import ConversationTextDAO
from backend.dao.files_dao import FilesDAO
from backend.dao.files_in_text_dao import FilesInTextDAO

from backend.services.conversation_service import ConversationService
from backend.services.upload_service import UploadService

from backend.routes.conversation_controller import ConversationController
from backend.routes.upload_controller import UploadController

from backend.config import get_db
from backend.const import UPLOAD_DIR

from ml_pipeline.llm.client import llm_client


os.makedirs(UPLOAD_DIR, exist_ok=True)



conversation_dao = ConversationDAO(get_db)
conversation_text_dao = ConversationTextDAO(get_db)
files_dao = FilesDAO(get_db)
files_in_text_dao = FilesInTextDAO(get_db)

llm_client_instance = llm_client() # ici on doit mettre le client llm
conversation_service = ConversationService(conversation_dao, conversation_text_dao, llm_client_instance, files_in_text_dao)
upload_service = UploadService(files_dao)


conversation_controller = ConversationController(conversation_service)
upload_controller = UploadController(upload_service)


app = FastAPI()


app.include_router(conversation_controller.router_api, prefix="/api")
app.include_router(upload_controller.router_api, prefix="/api")

