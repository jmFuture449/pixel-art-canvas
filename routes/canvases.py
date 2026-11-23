from flask import Blueprint, jsonify, request

from services.canvases import CanvasValidationError, save_canvas


canvases_bp = Blueprint("canvases", __name__)


@canvases_bp.post("/canvases")
def create_canvas():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Send a JSON object with a name and pixel_data."), 400

    try:
        canvas = save_canvas(payload.get("name"), payload.get("pixel_data"))
    except CanvasValidationError as error:
        return jsonify(error=str(error)), 400

    return jsonify(message="Canvas saved successfully.", id=canvas.id), 201
