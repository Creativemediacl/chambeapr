from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from urllib.parse import quote
from datetime import datetime, timedelta
from database import get_db
from models import Worker, Review
from schemas import WorkerCreate, WorkerPublic, ReviewCreate, ReviewPublic, LoginRequest, ForgotPasswordRequest
from passlib.context import CryptContext
from email_service import send_welcome_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter()

MUNICIPIOS = ["Adjuntas","Aguada","Aguadilla","Aguas Buenas","Aibonito","Anasco","Arecibo","Arroyo","Barceloneta","Barranquitas","Bayamon","Cabo Rojo","Caguas","Camuy","Canovanas","Carolina","Catano","Cayey","Ceiba","Ciales","Cidra","Coamo","Comerio","Corozal","Culebra","Dorado","Fajardo","Florida","Guanica","Guayama","Guayanilla","Guaynabo","Gurabo","Hatillo","Hormigueros","Humacao","Isabela","Jayuya","Juana Diaz","Juncos","Lajas","Lares","Las Marias","Las Piedras","Loiza","Luquillo","Manati","Maricao","Maunabo","Mayaguez","Moca","Morovis","Naguabo","Naranjito","Orocovis","Patillas","Penuelas","Ponce","Quebradillas","Rincon","Rio Grande","Sabana Grande","Salinas","San German","San Juan","San Lorenzo","San Sebastian","Santa Isabel","Toa Alta","Toa Baja","Trujillo Alto","Utuado","Vega Alta","Vega Baja","Vieques","Villalba","Yabucoa","Yauco"]

CATEGORIAS = ["Electricista","Plomero","Aire Acondicionado","Carpintero","Pintor","Techado","Construccion","Jardineria","Limpieza","Mudanzas","Fumigacion","Impermeabilizacion","Soldadura","Cerrajero","Reparacion de Electrodomesticos","Servicio de Piscina","Cocinero a Domicilio","Catering","Reposteria","Chef Privado","Meal Prep","Barbero a Domicilio","Maquillista","Masajista","Esteticista","Unas y Pedicure","Pestanas y Cejas","Trenzas y Extensiones","Servicios Digitales","Diseno Web","IT y Computadoras","Reparacion de Computadoras","Aplicaciones Moviles","Marketing Digital","Redes Sociales","Diseno Grafico","Publicidad","Fotografia Profesional","Video y Edicion","Produccion Musical","Clases Particulares","Clases de Musica","Clases de Idiomas","Preparacion de Examenes","Entrenador Personal","Yoga","Nutricionista","Meditacion","Cuidado de Mascotas","Peluqueria de Mascotas","Paseador de Perros","Veterinario a Domicilio","Cuidado de Adultos Mayores","Planchado y Lavanderia"]

@router.get("/workers", response_model=List[WorkerPublic])
def get_workers(municipality: Optional[str] = None, profession: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Worker).filter(Worker.is_active == True)
    if municipality:
        query = query.filter(Worker.municipality == municipality)
    if profession:
        query = query.filter(Worker.profession.contains(profession))
    return query.all()

@router.post("/workers", response_model=WorkerPublic)
def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    if not worker.accepted_terms:
        raise HTTPException(status_code=400, detail="Debes aceptar los terminos y condiciones")
    existing = db.query(Worker).filter(Worker.email == worker.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Este email ya esta registrado")
    trial_ends = datetime.utcnow() + timedelta(days=30)
    worker_data = worker.dict()
    password = worker_data.pop("password")
    hashed = pwd_context.hash(password)
    db_worker = Worker(**worker_data, trial_ends_at=trial_ends, hashed_password=hashed)
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

@router.get("/workers/by-email/{email}", response_model=WorkerPublic)
def get_worker_by_email(email: str, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.email == email).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Tecnico no encontrado")
    return worker

@router.get("/workers/{worker_id}", response_model=WorkerPublic)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Tecnico no encontrado")
    return worker

@router.get("/workers/{worker_id}/contact")
def contact_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Tecnico no encontrado")
    number = worker.whatsapp_number or worker.phone_number
    clean = number.replace("+","").replace(" ","").replace("-","")
    message = f"Hola {worker.full_name}, te contacto desde ChambeaPR. Vi tu perfil como {worker.profession} en {worker.municipality}. Estas disponible?"
    encoded = quote(message)
    return {"whatsapp_url": f"https://wa.me/{clean}?text={encoded}"}

@router.post("/reviews", response_model=ReviewPublic)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    db_review = Review(**review.dict())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

@router.get("/reviews/{worker_id}", response_model=List[ReviewPublic])
def get_reviews(worker_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.worker_id == worker_id).all()

@router.get("/municipios")
def get_municipios():
    return {"municipios": MUNICIPIOS}

@router.get("/categorias")
def get_categorias():
    return {"categorias": CATEGORIAS}


@router.post("/workers/deactivate/{email}")
def deactivate_worker(email: str, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.email == email).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Tecnico no encontrado")
    worker.is_active = False
    db.commit()
    return {"message": "Cuenta desactivada exitosamente"}


@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.email == request.email).first()
    if not worker:
        raise HTTPException(status_code=401, detail="Email o contrasena incorrectos")
    if not worker.hashed_password or not pwd_context.verify(request.password, worker.hashed_password):
        raise HTTPException(status_code=401, detail="Email o contrasena incorrectos")
    return {"success": True, "worker_id": worker.id, "full_name": worker.full_name}


@router.put("/workers/update/{email}")
def update_worker(email: str, data: dict, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.email == email).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Tecnico no encontrado")
    for key, value in data.items():
        if hasattr(worker, key) and value:
            setattr(worker, key, value)
    db.commit()
    return {"message": "Perfil actualizado exitosamente"}


import secrets

@router.post("/forgot-password")
def forgot_password(request: dict, db: Session = Depends(get_db)):
    email = request.get("email")
    worker = db.query(Worker).filter(Worker.email == email).first()
    if worker:
        token = secrets.token_urlsafe(32)
        worker.reset_token = token
        worker.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        db.commit()
        return {"message": "Enlace generado", "reset_url": f"https://chambeapr.com/reset-password?token={token}"}
    return {"message": "Email no encontrado"}


@router.post("/reset-password")
def reset_password(data: dict, db: Session = Depends(get_db)):
    token = data.get("token")
    password = data.get("password")
    worker = db.query(Worker).filter(Worker.reset_token == token).first()
    if not worker:
        raise HTTPException(status_code=400, detail="Token invalido")
    if worker.reset_token_expires < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expirado")
    worker.hashed_password = pwd_context.hash(password)
    worker.reset_token = None
    worker.reset_token_expires = None
    db.commit()
    return {"message": "Contrasena actualizada exitosamente"}
