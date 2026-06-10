import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routes.workers import router as workers_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TallerPR API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(workers_router, prefix="/api")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    path = os.path.join(os.getcwd(), "frontend", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)
