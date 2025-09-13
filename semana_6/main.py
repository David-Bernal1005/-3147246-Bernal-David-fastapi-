from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
from models import Base, Muestra
from schemas import MuestraCreate, MuestraResponse, UserRegister, UserLogin, Token
from database import get_db, engine
from pydantic import BaseModel
import uuid

app = FastAPI(title="API de Muestras Semana 6")
security = HTTPBearer()

# Simulación de usuarios en memoria
fake_users_db = {}

# Simulación de tokens
fake_tokens = {}

# -------------------------
# Autenticación básica
# -------------------------
@app.post("/register", response_model=Token)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username ya registrado")
    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "role": user.role
    }
    # Generar token simple
    token = str(uuid.uuid4())
    fake_tokens[token] = user.username
    return Token(access_token=token)

@app.post("/login", response_model=Token)
def login_user(user: UserLogin):
    db_user = fake_users_db.get(user.username)
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = str(uuid.uuid4())
    fake_tokens[token] = user.username
    return Token(access_token=token)

def get_current_user(token: str = Depends(security)):
    token_value = token.credentials
    username = fake_tokens.get(token_value)
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido")
    return fake_users_db[username]

# -------------------------
# CRUD de Muestra
# -------------------------
@app.post("/lab_muestra/", response_model=MuestraResponse, status_code=201)
def create_muestra(muestra: MuestraCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_muestra = db.query(Muestra).filter(Muestra.id == muestra.id).first()
    if db_muestra:
        raise HTTPException(status_code=400, detail="La muestra ya existe")
    obj = Muestra(**muestra.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@app.get("/lab_muestra/", response_model=List[MuestraResponse])
def get_all_muestras(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Muestra).all()

@app.get("/lab_muestra/{muestra_id}", response_model=MuestraResponse)
def get_muestra_by_id(muestra_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = db.query(Muestra).filter(Muestra.id == muestra_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Muestra no encontrada")
    return obj

@app.put("/lab_muestra/{muestra_id}", response_model=MuestraResponse)

def update_muestra(muestra_id: str, muestra: MuestraCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = db.query(Muestra).filter(Muestra.id == muestra_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Muestra no encontrada")
    # Permitir update parcial (PATCH-like)
    data = muestra.dict(exclude_unset=True)
    for key, value in data.items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/lab_muestra/{muestra_id}")

def delete_muestra(muestra_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    obj = db.query(Muestra).filter(Muestra.id == muestra_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Muestra no encontrada")
    # Solo admin puede eliminar
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar muestras")
    db.delete(obj)
    db.commit()
    return {"detail": "Muestra eliminada"}
