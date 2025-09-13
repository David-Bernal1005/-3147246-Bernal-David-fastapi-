

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from models import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_muestra.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

# FIXTURE ESPECÍFICA PARA TU DOMINIO
@pytest.fixture
def sample_muestra_data():
    """
    Datos de ejemplo específicos para Muestra
    🚨 PERSONALIZAR COMPLETAMENTE SEGÚN TU NEGOCIO
    """
    return {
        "id": "1",
        "tipo_de_muestra": "sangre",
        "cantidad": 5.0,
        "tipo_de_sangre": "A+",
        "fecha_de_recoleccion": "2023-10-01",
    }

@pytest.fixture
def auth_headers(client):
    """Headers de autenticación para tests"""
    # Crear usuario de prueba específico para tu dominio
    response = client.post("/register", json={
        "username": "admin_muestra",
        "email": "admin@example.com",
        "password": "test123",
        "role": "admin"
    })
    login_response = client.post("/login", json={
        "username": "admin_muestra",
        "password": "test123"
    })
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}