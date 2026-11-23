import re

from models import Canvas, db


GRID_SIZE = 32
HEX_COLOR = re.compile(r"^#[0-9a-fA-F]{6}$")


class CanvasValidationError(ValueError):
    """Raised when submitted canvas data is invalid."""


def save_canvas(name, pixel_data):
    if not isinstance(name, str) or not name.strip():
        raise CanvasValidationError("Enter a name for your canvas.")
    name = name.strip()
    if len(name) > 120:
        raise CanvasValidationError("Canvas names must be 120 characters or fewer.")

    if (
        not isinstance(pixel_data, list)
        or len(pixel_data) != GRID_SIZE
        or any(not isinstance(row, list) or len(row) != GRID_SIZE for row in pixel_data)
    ):
        raise CanvasValidationError("Canvas data must be a 32×32 grid.")

    for row in pixel_data:
        if any(not isinstance(color, str) or not HEX_COLOR.fullmatch(color) for color in row):
            raise CanvasValidationError("Every pixel must have a valid hex colour.")

    canvas = Canvas(name=name, pixel_data=pixel_data)
    db.session.add(canvas)
    db.session.commit()
    return canvas
