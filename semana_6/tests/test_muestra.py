import pytest
from fastapi.testclient import TestClient

class TestmuestraAPI:
    def get_admin_headers(self, client):
        response = client.post("/register", json={
            "username": "admin_muestra2",
            "email": "admin2@example.com",
            "password": "adminpass",
            "role": "admin"
        })
        login_response = client.post("/login", json={
            "username": "admin_muestra2",
            "password": "adminpass"
        })
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def get_user_headers(self, client):
        response = client.post("/register", json={
            "username": "user_muestra",
            "email": "user@example.com",
            "password": "userpass",
            "role": "usuario_laboratorio"
        })
        login_response = client.post("/login", json={
            "username": "user_muestra",
            "password": "userpass"
        })
        token = login_response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_admin_can_delete_muestra(self, client):
        """Test que solo admin puede eliminar muestra"""
        admin_headers = self.get_admin_headers(client)
        # Crear muestra
        data = {
            "id": "admin_del",
            "tipo_de_muestra": "sangre",
            "cantidad": 5.0,
            "tipo_de_sangre": "A+",
            "fecha_de_recoleccion": "2023-10-10",
        }
        client.post("/lab_muestra/", json=data, headers=admin_headers)
        # Eliminar como admin
        response = client.delete(f"/lab_muestra/admin_del", headers=admin_headers)
        assert response.status_code == 200
        assert "eliminada" in response.json()["detail"].lower()

    def test_regular_user_cannot_delete_muestra(self, client):
        """Test que usuario regular no puede eliminar muestra"""
        admin_headers = self.get_admin_headers(client)
        user_headers = self.get_user_headers(client)
        # Crear muestra como admin
        data = {
            "id": "user_no_del",
            "tipo_de_muestra": "orina",
            "cantidad": 3.0,
            "tipo_de_sangre": "O-",
            "fecha_de_recoleccion": "2023-10-11",
        }
        client.post("/lab_muestra/", json=data, headers=admin_headers)
        # Intentar eliminar como usuario regular
        response = client.delete(f"/lab_muestra/user_no_del", headers=user_headers)
        assert response.status_code in (401, 403)
    def test_create_muestra_success(self,client,sample_muestra_data,auth_headers):
        response = client.post(f"/lab_muestra/", json=sample_muestra_data, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()

        assert data["id"] == sample_muestra_data["id"]
        assert data["tipo_de_muestra"] == sample_muestra_data["tipo_de_muestra"]
        assert data["cantidad"] == sample_muestra_data["cantidad"]
        assert data["tipo_de_sangre"] == sample_muestra_data["tipo_de_sangre"]
        assert data["fecha_de_recoleccion"] == sample_muestra_data["fecha_de_recoleccion"]
    
    def test_get_muestra_not_found(self,client,auth_headers):
        response = client.get(f"/lab_muestra/nonexistent_id", headers=auth_headers)
        assert response.status_code == 404
        assert "muestra no encontrada" in response.json()["detail"].lower()

    def test_muestra_validation_error(self,client,auth_headers):
        invalid_data = {
            "id": "2",
            "tipo_de_muestra": "orina",
            "cantidad": -5.0,  # Cantidad inválida
            "tipo_de_sangre": "O+",
            "fecha_de_recoleccion": "2023-10-02",
        }
        response = client.post(f"/lab_muestra/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422
        errors = response.json()["detail"]
        assert any("id" in str(error) for error in errors)

    def test_create_muestra_complete(self,client,auth_headers):
        data = {
            "id": "3",
            "tipo_de_muestra": "saliva",
            "cantidad": 10.0,
            "tipo_de_sangre": "B+",
            "fecha_de_recoleccion": "2023-10-03",
        }
        response = client.post(f"/lab_muestra/", json=data, headers=auth_headers)
        assert response.status_code == 201
        created = response.json()

        assert created["id"] == data["id"]
        assert "id" in created
    def test_create_muestra_duplicate(self,client,auth_headers):
        data = {
            "id": "1",  # Mismo ID que en sample_muestra_data
            "tipo_de_muestra": "sangre",
            "cantidad": 5.0,
            "tipo_de_sangre": "A+",
            "fecha_de_recoleccion": "2023-10-01",
        }
        
        client.post(f"/lab_muestra/", json=data, headers=auth_headers)  # Crear la primera vez
        response = client.post(f"/lab_muestra/", json=data, headers=auth_headers)
        
        assert response.status_code == 400
        assert "ya existe" in response.json()["detail"].lower()
    
    def test_get_muestra_by_id(self,client,auth_headers):
        create_data = {
            "id": "4",
            "tipo_de_muestra": "tejido",
            "cantidad": 15.0,
            "tipo_de_sangre": "AB+",
            "fecha_de_recoleccion": "2023-10-04",
        }
        create_response = client.post(f"/lab_muestra/", json=create_data, headers=auth_headers)
        created_id = create_response.json()["id"]

        response = client.get(f"/lab_muestra/{created_id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == created_id
    
    def test_get_all_muestras(self,client,auth_headers):
        response = client.get(f"/lab_muestra/", headers=auth_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_muestra_not_found(self,client,auth_headers):
        response = client.get(f"/lab_muestra/nonexistent_id", headers=auth_headers)
        assert response.status_code == 404
        assert "muestra no encontrada" in response.json()["detail"].lower()

    def test_update_muestra_complete(self, client, auth_headers):
        create_data = {
            "id": "5",
            "tipo_de_muestra": "sangre",
            "cantidad": 20.0,
            "tipo_de_sangre": "A-",
            "fecha_de_recoleccion": "2023-10-05",
        }
        create_response = client.post(f"/lab_muestra/", json=create_data, headers=auth_headers)
        entity_id = create_response.json()["id"]

        update_data = {
            "tipo_de_muestra": "orina",
            "cantidad": 25.0,
            "tipo_de_sangre": "B-",
            "fecha_de_recoleccion": "2023-10-06",
        }
        response = client.put(f"/lab_muestra/{entity_id}", json={"id": entity_id, **update_data}, headers=auth_headers)
        assert response.status_code == 200
        updated = response.json()

    def test_delete_muestra_success(self, client, auth_headers):
        create_data = {
            "id": "6",
            "tipo_de_muestra": "saliva",
            "cantidad": 30.0,
            "tipo_de_sangre": "O-",
            "fecha_de_recoleccion": "2023-10-07",
        }
        create_response = client.post(f"/lab_muestra/", json=create_data, headers=auth_headers)
        entity_id = create_response.json()["id"]

        response = client.delete(f"/lab_muestra/{entity_id}", headers=auth_headers)
        assert response.status_code == 200
        assert "eliminada" in response.json()["detail"].lower()

        get_response = client.get(f"/lab_muestra/{entity_id}", headers=auth_headers)
        assert get_response.status_code == 404
    def test_delete_muestra_not_found(self, client, auth_headers):
        response = client.delete(f"/lab_muestra/nonexistent_id", headers=auth_headers)
        assert response.status_code == 404
        assert "muestra no encontrada" in response.json()["detail"].lower()
    
    def test_muestra_business_rules(self, client, auth_headers):
        invalid_data = {
            "id": "7",
            "tipo_de_muestra": "sangre",
            "cantidad": -10.0,  
            "tipo_de_sangre": "AB-",
            "fecha_de_recoleccion": "2023-10-08",
        }
        response = client.post(f"/lab_muestra/", json=invalid_data, headers=auth_headers)
        assert response.status_code == 422        