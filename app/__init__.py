from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from sqlalchemy import text  # <-- voor health-check query
from config import Config
from models import db, Artists, SuggestionFeedback  # gebruik dezelfde db als in models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # extensies koppelen
    db.init_app(app)
    Migrate(app, db)

    # HOME: endpoint expliciet 'editions' (matcht je templates)
    @app.get("/", endpoint="editions")     # <-- 'endpoint', niet 'endpoints'
    def home():
        return render_template("editions.html")

    # HEALTH: simpele DB-check
    @app.get("/health")
    def health():
        try:
            db.session.execute(text("select 1"))  # <-- gebruik sqlalchemy.text
            return {"status": "ok"}, 200
        except Exception as e:
            return {"status": "error", "detail": str(e)}, 500

    # SUGGEST: formulier voor artiest-voorstel
    @app.route("/suggest", methods=["GET", "POST"])
    def suggest():
        if request.method == "POST":
            artist_name = request.form.get("artist_name", "").strip()
            if not artist_name:
                flash("Geef een artiestnaam op.", "warning")
                return redirect(url_for("suggest"))

            a = Artists(Artist_name=artist_name)
            db.session.add(a)
            db.session.commit()

            s = SuggestionFeedback(artist_id=a.id)
            db.session.add(s)
            db.session.commit()

            flash("Bedankt voor je suggestie!", "success")
            return redirect(url_for("editions"))  # werkt nu: endpoint bestaat
        return render_template("suggest.html")

    return app  # <-- binnen de functie blijven!
