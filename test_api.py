from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Test de la redirection vers /docs
def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    assert response.url == "http://testserver/docs"


# Test de l'ajout d'une nouvelle entrée
def test_add_entry():
    response = client.get("/add", params={
        "tag": "test_tag",
        "enable": 1,
        "dns": "8.8.8.8",
        "priority": 2,
        "period": 60
    })
    assert response.status_code == 200
    assert response.text == '"Added"'


# Test de la suppression d'une entrée
def test_delete_entry():
    # Ajoutez une entrée pour la supprimer ensuite
    client.get("/add", params={
        "tag": "delete_tag",
        "enable": 1,
        "dns": "8.8.4.4",
        "priority": 3,
        "period": 120
    })

    response = client.get("/delete", params={"tag": "delete_tag"})
    assert response.status_code == 200
    assert response.text == '"Deleted"'


# Test de la mise à jour d'une entrée
def test_update_entry():
    # Ajoutez une entrée pour la mettre à jour ensuite
    client.get("/add", params={
        "tag": "update_tag",
        "enable": 1,
        "dns": "1.1.1.1",
        "priority": 2,
        "period": 60
    })

    response = client.get("/update", params={
        "tag": "update_tag",
        "enable": 0,
        "dns": "9.9.9.9",
        "priority": 1,
        "period": 30
    })
    assert response.status_code == 200
    assert response.text == '"Updated"'


# Test des valeurs limites pour les priorités
def test_add_invalid_priority():
    response = client.get("/add", params={
        "tag": "invalid_priority",
        "enable": 1,
        "dns": "8.8.8.8",
        "priority": 5,  # Valeur invalide
        "period": 60
    })
    assert response.status_code == 200
    assert response.text == '"Priority should be between 1 and 4"'


# Test d'une entrée qui n'existe pas
def test_delete_nonexistent_entry():
    response = client.get("/delete", params={"tag": "nonexistent_tag"})
    assert response.status_code == 200
    assert response.text == '"Label nonexistent_tag doesn\'t exist!"'
