from tests.conftest import client

def test_create_transaction(test_user_token):
    response = client.post("/transactions/", json={
        "title": "Lunch", "amount": 15.50, "type": "expense",
        "category": "Food", "date": "2025-01-01"
    }, headers=test_user_token)
    assert response.status_code == 200
    assert response.json()["title"] == "Lunch"

def test_get_all_transactions(test_user_token):
    response = client.get("/transactions/", headers=test_user_token)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_specific_transaction(test_user_token):
    # First create one
    create_res = client.post("/transactions/", json={
        "title": "Book", "amount": 20.0, "type": "expense",
        "category": "Education", "date": "2025-01-02"
    }, headers=test_user_token)
    trans_id = create_res.json()["id"]
    
    response = client.get(f"/transactions/{trans_id}", headers=test_user_token)
    assert response.status_code == 200
    assert response.json()["id"] == trans_id

def test_update_transaction(test_user_token):
    create_res = client.post("/transactions/", json={
        "title": "Old Title", "amount": 10.0, "type": "expense",
        "category": "Misc", "date": "2025-01-03"
    }, headers=test_user_token)
    trans_id = create_res.json()["id"]
    
    response = client.put(f"/transactions/{trans_id}", json={
        "title": "New Title", "amount": 12.0
    }, headers=test_user_token)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["amount"] == 12.0

def test_delete_transaction(test_user_token):
    create_res = client.post("/transactions/", json={
        "title": "To Delete", "amount": 5.0, "type": "expense",
        "category": "Test", "date": "2025-01-04"
    }, headers=test_user_token)
    trans_id = create_res.json()["id"]
    
    response = client.delete(f"/transactions/{trans_id}", headers=test_user_token)
    assert response.status_code == 200
    
    # Verify it's gone
    get_res = client.get(f"/transactions/{trans_id}", headers=test_user_token)
    assert get_res.status_code == 404