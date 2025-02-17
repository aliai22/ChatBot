from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.api.endpoints import upload, chatbot
from app.services.llm import startup_event

app = FastAPI(on_startup=[startup_event])  # Ensure model is loaded asynchronously

# Mount templates folder
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(upload.router, prefix="/api")
app.include_router(chatbot.router, prefix="/api")  # Add chatbot API

@app.get("/")
async def upload_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})