import sys
import uuid
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from models import Canvas, db


@pytest.fixture
def client():
    database_path = PROJECT_ROOT / f"test_pixel_art_{uuid.uuid4().hex}.db"
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path.as_posix()}",
    })

    with app.app_context():
        db.create_all()

    with app.test_client() as test_client:
        yield test_client

    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    database_path.unlink(missing_ok=True)


def valid_grid():
    return [["#ffffff" for _ in range(32)] for _ in range(32)]


def test_create_canvas_saves_valid_canvas(client):
    response = client.post(
        "/canvases",
        json={"name": "  Tiny landscape  ", "pixel_data": valid_grid()},
    )

    assert response.status_code == 201
    assert response.json["message"] == "Canvas saved successfully."
    with client.application.app_context():
        saved = db.session.get(Canvas, response.json["id"])
        assert saved.name == "Tiny landscape"
        assert saved.pixel_data == valid_grid()


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"name": "", "pixel_data": valid_grid()}, "Enter a name for your canvas."),
        ({"name": "Valid name", "pixel_data": [["#ffffff"]]}, "Canvas data must be a 32×32 grid."),
        (
            {"name": "Valid name", "pixel_data": [["invalid" for _ in range(32)] for _ in range(32)]},
            "Every pixel must have a valid hex colour.",
        ),
    ],
)
def test_create_canvas_rejects_invalid_payload(client, payload, message):
    response = client.post("/canvases", json=payload)

    assert response.status_code == 400
    assert response.json["error"] == message


def test_create_canvas_rejects_non_object_json(client):
    response = client.post("/canvases", data="[]", content_type="application/json")

    assert response.status_code == 400
    assert "JSON object" in response.json["error"]
