from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field
import shutil
from pathlib import Path
from backend.service.bot_service import bot_service
# from backend.model.bot_interaction import UserQuery, BotReply

app = FastAPI()

class UserQuery(BaseModel):
    index: int = Field(..., description="Message index in the conversation")
    content: str = Field(..., description="Content of the user message")


class BotReply(BaseModel):
    index: int = Field(..., description="Message index in the conversation")
    content: str = Field(..., description="Content of the bot reply")


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI!"}

@app.post("/bot-reply", response_model=BotReply)
async def chat(user_input: UserQuery):
    reply_content = bot_service.reply(user_input.content)
    return BotReply(index=user_input.index, content=reply_content)


UPLOADED_PDF_DIR = Path("uploaded_pdfs")
UPLOADED_PDF_DIR.mkdir(exist_ok=True)

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # Save file to disk
    file_path = UPLOADED_PDF_DIR / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "saved_path": str(file_path)}