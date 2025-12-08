from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# ------------------------------
# BACKEND IMPORTS (AS YOU HAD)
# ------------------------------
from dao.conversations_dao import ConversationDAO
from dao.conversation_text_dao import ConversationTextDAO
from dao.files_dao import FilesDAO
from dao.files_in_text_dao import FilesInTextDAO
from services.conversation_service import ConversationService
from services.upload_service import UploadService
from routes.conversation_controller import ConversationController
from routes.upload_controller import UploadController
from config import get_db, settings
from const import UPLOAD_DIR

from llm.client import LLM
from retrieval.retriever import rag


# ------------------------------
# INITIAL SETUP
# ------------------------------
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI()

# STATIC + TEMPLATE SUPPORT
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ------------------------------
# LLM ADAPTER
# ------------------------------
class SimpleLLMAdapter:
    def __init__(self):
        tools = [rag]
        self.llm = LLM(tools, "mistral-large-latest")
        self.agent = self.llm.get_agent()
    
    def call_llm(self, user_input):
        response = self.agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            {"configurable": {"thread_id": "1"}}
        )
        
        ai_text = response["messages"][-1].content
        return {"text": ai_text, "files": []}


llm_client = SimpleLLMAdapter()


# ------------------------------
# BUILD SERVICES
# ------------------------------
conversation_service = ConversationService(
    ConversationDAO(get_db),
    ConversationTextDAO(get_db),
    llm_client,
    FilesInTextDAO(get_db)
)

upload_service = UploadService(FilesDAO(get_db))

conversation_controller = ConversationController(conversation_service)
upload_controller = UploadController(upload_service)


# ------------------------------
# CORS (NE PAS TOUCHER)
# ------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------------
# API ROUTES
# ------------------------------
app.include_router(conversation_controller.router_api, prefix="/api")
app.include_router(upload_controller.router_api, prefix="/api")


# ------------------------------
# FRONTEND ROUTES
# ------------------------------

@app.get("/", response_class=HTMLResponse)
def home():
    """Simple menu page"""
    return """
    <html>
    <body style='font-family:Arial; padding:20px'>
        <h1>RecruitAI – Interface</h1>
        <p><a href='/chat'>💬 Chatbot</a></p>
        <p><a href='/upload'>📄 Upload CV</a></p>
    </body>
    </html>
    """


@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    """Load templates/chat.html"""
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/upload", response_class=HTMLResponse)
def upload_page(request: Request):
    """Load templates/upload.html"""
    return templates.TemplateResponse("upload.html", {"request": request})



@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})


# ------------------------------
# HEALTH CHECK
# ------------------------------
@app.get("/api/health")
def health():
    return {"status": "ok"}





# from pipeline.rag_pipeline import RAGPipeline
# from config.settings import settings
# import os

# def initVectorDataBase():
#     print("🚀 Initialisation de la base vectorielle...")

#     data_path = settings.DATA_PATH

#     if not os.path.exists(data_path):
#         raise Exception(f" DATA_PATH introuvable : {data_path}")

#     pipeline = RAGPipeline(
#         base_path=data_path,
#         vector_db="qdrant"
#     )


#     pipeline.run()

#     print(" Vector store construit avec succès !")




# @app.on_event("startup")
# async def startup_event():
#     FIRST_TIME = True

#     if FIRST_TIME:
#         asyncio.create_task(async_init_vector_db())

        
        
        

# import asyncio
# from qdrant_client import QdrantClient

# async def wait_for_qdrant():
#     client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

#     for i in range(10):
#         try:
#             client.get_collections()
#             print(" Qdrant est prêt.")
#             return
#         except Exception:
#             print(f" Qdrant pas encore prêt… tentative {i+1}/10")
#             await asyncio.sleep(1)

#     raise RuntimeError(" Qdrant ne répond pas.")


# async def async_init_vector_db():
#     await wait_for_qdrant()

#     loop = asyncio.get_event_loop()
#     print(" Construction de la base vectorielle en arrière-plan…")

#     await loop.run_in_executor(None, initVectorDataBase)

#     print(" Base vectorielle prête !")
