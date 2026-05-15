import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import engine
import models
from routers import auth as auth_router
from routers import teams as teams_router
from routers import tasks as tasks_router
from routers import messages as messages_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="TaskFlow MVP")

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(teams_router.router)
app.include_router(tasks_router.router)
app.include_router(messages_router.router)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/signup")
def signup_page():
    return FileResponse(os.path.join(static_dir, "signup.html"))

@app.get("/teams")
def teams_page():
    return FileResponse(os.path.join(static_dir, "teams.html"))

@app.get("/kanban")
def kanban_page():
    return FileResponse(os.path.join(static_dir, "kanban.html"))

@app.get("/chat")
def chat_page():
    return FileResponse(os.path.join(static_dir, "chat.html"))
