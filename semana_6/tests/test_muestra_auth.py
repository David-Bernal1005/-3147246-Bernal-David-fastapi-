def test_register_laboratorio_user(client):
    data = {
        "id": "4",
        "username": "panchito",
        "password": "777222",
        "email": "panchito@example.com",
        "role": "usuario_laboratorio",
        "id_muestra": "1"
    }

    response = client.post("/register", json={**data, "email": "panchito@example.com"})
    assert response.status_code == 200

def test_login_laboratorio_user(client):
    register_data = {
        "id": "5",
        "username": "pepito_lab",
        "password": "888333",
        "email": "pepito_lab@example.com",
        "role": "admin_laboratorio"
    }
    client.post("/register", json={**register_data, "email": "pepito_lab@example.com"})
    login_data = {
        "username": "pepito_lab",
        "password": "888333"
    }
    response = client.post("/login", json=login_data)

    assert response.status_code == 200
    assert "access_token" in response.json()

def test_Laboratorio_permissions(client,auth_headers):
     roles={
         "admin_laboratorio": ["create", "read", "update", "delete"],
         "usuario_laboratorio": ["read"]
     }

def test_user_access_restriction(client):
    response = client.get("/lab_muestra/")
    assert response.status_code == 403

def test_create_muestra_requires_auth(client):
    data = {
        "id": "2",
        "tipo_de_muestra": "orina",
        "cantidad": 3.0,
        "tipo_de_sangre": "O-",
        "fecha_de_recoleccion": "2023-10-02",
    }
    response = client.post(f"/lab_muestra/", json=data)
    assert response.status_code == 403

def test_admin_can_delete_muestra(client,auth_headers):
    admin_headers = auth_headers