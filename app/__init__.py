from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# maak de extensies één keer aan (module-level),
# zodat wsgi.py 'db' kan importeren
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialiseer extensies met deze app
    db.init_app(app)
    migrate.init_app(app, db)

    # eenvoudige routes om te testen
    @app.get("/")
    def home():
        return render_template("index.html")

    @app.get("/health")
    def health():
        try:
            db.session.execute(db.text("select 1"))
            return {"status": "ok"}, 200
        except Exception as e:
            return {"status": "error", "detail": str(e)}, 500

    return app
