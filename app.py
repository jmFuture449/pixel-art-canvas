from pathlib import Path

from flask import Flask, render_template

from models import db


def create_app():
    app = Flask(__name__)
    database_path = Path(__file__).with_name("pixel_art.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path.as_posix()}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    @app.get("/")
    def index():
        return render_template("index.html")

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=False)
