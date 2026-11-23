from pathlib import Path

from flask import Flask, render_template

from models import db
from routes.canvases import canvases_bp


def create_app(test_config=None):
    app = Flask(__name__)
    database_path = Path(__file__).with_name("pixel_art.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path.as_posix()}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    app.register_blueprint(canvases_bp)

    @app.get("/")
    def index():
        return render_template("index.html")

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=False)
