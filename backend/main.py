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

def serve_html(filename):
    path = os.path.join(os.getcwd(), "frontend", filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

@app.get("/")
def read_root():
    return serve_html("index.html")

@app.get("/subscribe")
def subscribe_page():
    return serve_html("subscribe.html")

@app.get("/terms")
def terms_page():
    return serve_html("terms.html")

@app.get("/privacy")
def privacy_page():
    return serve_html("privacy.html")

@app.get("/success")
def success_page():
    return HTMLResponse(content="<html><body style='font-family:Arial;text-align:center;padding:50px;background:#1B2A4A;color:white'><h1 style='color:#F5A623'>Bienvenido a ChambeaPR Pro!</h1><p style='color:#ccd6f6;margin-top:15px;'>Tu suscripcion ha sido activada exitosamente.</p><br><a href='/' style='background:#F5A623;color:#1B2A4A;padding:12px 25px;border-radius:10px;text-decoration:none;font-weight:bold;'>Volver al inicio</a></body></html>")

@app.get("/dashboard")
def dashboard_page():
    return serve_html("dashboard.html")

@app.get("/edit-profile")
def edit_profile_page():
    return serve_html("edit-profile.html")

@app.get("/forgot-password")
def forgot_password_page():
    return serve_html("forgot-password.html")

@app.get("/reset-password")
def reset_password_page():
    return serve_html("reset-password.html")
