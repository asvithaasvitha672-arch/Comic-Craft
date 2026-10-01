import os

# Run application tests without external APIs.
os.environ["MOCK_MODE"] = "true"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "ComicCraft" in response.text


def test_json_validation_rejects_empty_prompt():

    response = client.post(
        "/generate-comic/json",

        json={
            "story_prompt": "",

            "character_name": "Luna",

            "setting": "Forest",

            "tone": "Funny",

            "art_style": "Anime",
        },
    )

    assert response.status_code == 422