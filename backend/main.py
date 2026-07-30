import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routes.workers import router as workers_router
from routes.payments import router as payments_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ChambeaPR API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(workers_router, prefix="/api")
app.include_router(payments_router, prefix="/api")

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    path = os.path.join(os.getcwd(), "frontend", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/subscribe")
def subscribe_page():
    path = os.path.join(os.getcwd(), "frontend", "subscribe.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/success")
def success_page():
    return HTMLResponse(content="<html><body style='font-family:Arial;text-align:center;padding:50px;background:#1B2A4A;color:white'><h1 style='color:#F5A623'>Bienvenido a ChambeaPR Pro!</h1><p>Tu suscripcion ha sido activada exitosamente.</p><a href='/' style='color:#F5A623'>Volver al inicio</a></body></html>")
