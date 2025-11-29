import sys
import os
import pytest
from fastapi.testclient import TestClient

# Add backend to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_emergency_flow():
    # 1. Start Session
    response = client.post("/new-session")
    assert response.status_code == 200
    session_id = response.json()["session_id"]
    print(f"Session ID: {session_id}")

    # 2. Start Incident
    response = client.post("/agent", json={"session_id": session_id, "message": "Help, I had an accident"})
    assert response.status_code == 200
    print(f"Bot: {response.json()['text']}")
    assert "describe what happened" in response.json()["text"].lower()

    # 3. Triage (High Severity)
    response = client.post("/agent", json={"session_id": session_id, "message": "I am bleeding heavily from a deep cut on my leg"})
    assert response.status_code == 200
    print(f"Bot: {response.json()['text']}")
    assert "serious" in response.json()["text"].lower() or "ambulance" in response.json()["text"].lower()

    # 4. Location
    response = client.post("/agent", json={"session_id": session_id, "message": "I am at 123 Main St, Springfield"})
    assert response.status_code == 200
    print(f"Bot: {response.json()['text']}")
    # Should mention dispatch or location received
    assert "dispatch" in response.json()["text"].lower() or "location" in response.json()["text"].lower()

    # 5. First Aid
    response = client.post("/agent", json={"session_id": session_id, "message": "What should I do now?"})
    assert response.status_code == 200
    print(f"Bot: {response.json()['text']}")
    # Should provide first aid instruction
    assert len(response.json()["text"]) > 10

if __name__ == "__main__":
    test_emergency_flow()
