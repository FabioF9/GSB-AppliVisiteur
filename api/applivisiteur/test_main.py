import pytest
from fastapi.testclient import TestClient
from .main import app
from . import models, schemas

client = TestClient(app)

# Test pour vérifier si tous les rapports sont récupérés avec succès
def test_get_all_rapports():
    # Vous pouvez vous authentifier en envoyant un nom d'utilisateur et un mot de passe valide pour obtenir le token
    login_response = client.post("/login", data={"username": "demo", "password": "password"})
    print(login_response)
    token = login_response.json()[0]["access_token"]

    # Utilisez ce token dans l'en-tête Authorization pour les requêtes suivantes
    response = client.get("/rapports", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

# Test pour vérifier si un rapport spécifique est récupéré avec succès
def test_get_rapport_by_id():
    login_response = client.post("/login", data={"username": "demo", "password": "password"})
    print(login_response)
    token = login_response.json()[0]["access_token"]
    # Supposons que l'ID 1 existe dans la base de données
    response = client.get("/rapport/1",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

# Test pour vérifier la création d'un nouveau rapport
def test_create_rapport():
    login_response = client.post("/login", data={"username": "demo", "password": "password"})
    print(login_response)
    token = login_response.json()[0]["access_token"]

    rapport_data = {
        "RAP_DATE": "2024-02-13",
        "RAP_BILAN": "Test bilan",
        "RAP_MOTIF": "Test motif",
        "RAP_COMMENTAIRE": "Test commentaire",
        "MED_ID": 1,
        "VIS_MATRICULE": 1
    }
    response = client.post("/create_rapport", json=rapport_data,headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["RAP_DATE"] == "2024-02-13"


# Test pour vérifier la mise à jour d'un rapport existant
def test_update_rapport():
    login_response = client.post("/login", data={"username": "demo", "password": "password"})
    print(login_response)
    token = login_response.json()[0]["access_token"]
    # Supposons que l'ID 1 existe dans la base de données
    updated_rapport_data = {
        "RAP_DATE": "2024-02-14",
        "RAP_BILAN": "Updated bilan",
        "RAP_MOTIF": "Updated motif",
        "RAP_COMMENTAIRE": "Updated commentaire",
        "MED_ID": 2,
        "VIS_MATRICULE": 2
    }
    response = client.put("/update_rapport/1", json=updated_rapport_data,headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 202

# Test pour vérifier la suppression d'un rapport existant
def test_delete_rapport():
    login_response = client.post("/login", data={"username": "demo", "password": "password"})
    print(login_response)
    token = login_response.json()[0]["access_token"]
    # Supposons que l'ID 1 existe dans la base de données
    response = client.delete("/delete_rapport/1",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

# Test pour vérifier si le rapport maximum est récupéré avec succès
def test_get_max_rapport():
    login_response = client.post("/login", data={"username": "demo", "password": "password"})
    print(login_response)
    token = login_response.json()[0]["access_token"]
    # Supposons qu'il y a au moins un rapport dans la base de données
    response = client.get("/maxrapport",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json() >= 0  # Assurez-vous que le résultat est un nombre positif

# Test pour vérifier si un rapport spécifique créé par un visiteur est récupéré avec succès
def test_get_rapport_by_visiteur():
    login_response = client.post("/login", data={"username": "demo", "password": "password"})
    print(login_response)
    token = login_response.json()[0]["access_token"]
    # Supposons que le matricule du visiteur 1 existe dans la base de données
    response = client.get("/rapport/visiteur/1",headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) > 0

