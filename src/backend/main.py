from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import mysql.connector
import os

from dao.conversations_dao import ConversationDAO
from dao.conversation_text_dao import ConversationTextDAO
from dao.files_dao import FilesDAO
from dao.files_in_text_dao import FilesInTextDAO

from services.conversation_service import ConversationService
from services.upload_service import UploadService

from routes.conversation_controller import ConversationController
from routes.upload_controller import UploadController

from config import db

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

conversation_dao = ConversationDAO(db)
conversation_text_dao = ConversationTextDAO(db)
files_dao = FilesDAO(db)
files_in_text_dao = FilesInTextDAO(db)

llm_client = None # ici on doit mettre le client llm
conversation_service = ConversationService(conversation_dao, conversation_text_dao, llm_client, files_in_text_dao)
upload_service = UploadService(files_dao)


conversation_controller = ConversationController(conversation_service)
upload_controller = UploadController(upload_service)


app = FastAPI()


app.include_router(conversation_controller.router_api, prefix="/api")
app.include_router(upload_controller.router_api, prefix="/api")


app.mount("/", StaticFiles(directory="build"), name="frontend") # pour les fichier frontend

