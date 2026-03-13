# интеграционный тест
import pytest

def test_create_task(client):
    # 1. Сначала регистрируем и логиним пользователя (упростим для теста)
    client.post("/auth/register", json={"email": "test@test.com", "password": "password"})
    login_res = client.post("/auth/login", data={"username": "test@test.com", "password": "password"})
    token = login_res.json()["access_token"]
    
    # 2. Создаем задачу
    headers = {"Authorization": f"Bearer {token}"}
    task_data = {
        "title": "Test Task",
        "description": "Verify testing works",
        "priority": "high"
    }
    
    response = client.post("/tasks/", json=task_data, headers=headers)
    
    # 3. Проверяем результат
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["priority"] == "high"
    assert "id" in data

def test_update_task(client):
    # 1. Регистрация с УНИКАЛЬНЫМ email
    email = "update_test_unique@example.com"
    password = "strong_password_123"
    
    reg_res = client.post("/auth/register", json={"email": email, "password": password})
    assert reg_res.status_code == 201

    # 2. Логин (OAuth2 ожидает форму, поэтому используем data=)
    login_res = client.post("/auth/login", data={"username": email, "password": password})
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Создаем задачу
    task_res = client.post("/tasks/", json={"title": "Old Title", "priority": "low"}, headers=headers)
    assert task_res.status_code == 201
    task_id = task_res.json()["id"]

    # 4. Обновляем статус
    update_res = client.patch(f"/tasks/{task_id}", json={"status": "completed"}, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "completed"

def test_delete_task(client):
    # 1. Регистрация и логин с другим УНИКАЛЬНЫМ email
    email = "delete_test_unique@example.com"
    password = "strong_password_123"
    
    client.post("/auth/register", json={"email": email, "password": password})
    login_res = client.post("/auth/login", data={"username": email, "password": password})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Создаем задачу
    task_res = client.post("/tasks/", json={"title": "Delete Me", "priority": "medium"}, headers=headers)
    task_id = task_res.json()["id"]

    # 3. Удаляем
    delete_res = client.delete(f"/tasks/{task_id}", headers=headers)
    assert delete_res.status_code == 200
    
    # 4. Проверяем, что в списке пусто
    get_res = client.get("/tasks/", headers=headers)
    assert len(get_res.json()) == 0