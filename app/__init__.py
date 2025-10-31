from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from sqlalchemy import text
from config import Config
from models import db, Artists, SuggestionFeedback
from flask import session
from sqlalchemy import select 
from flask import request, redirect, url_for, flash, render_template
from datetime import date
from models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    def get_session_user():
        """Geef de huidige sessie-user (of None)."""
        uid = session.get("user_id")
        return db.session.get(User, uid) if uid else None

    def login_user(user: User):
        """Bewaar user.id in de sessie."""
        session["user_id"] = user.id

    def logout_user():
        """Verwijder user uit de sessie."""
        session.pop("user_id", None)

    def get_or_create_session_user():
        """Geef iedereen een user_id in de sessie (anoniem)."""
        uid = session.get("user_id")
        if uid is not None:
            return db.session.get(User, uid)

        u = User()  # lege user (geen email)
        db.session.add(u); db.session.commit()
        session["user_id"] = u.id
        return u

    def require_admin():
        """Heel simpele check (we houden het bewust basic)."""
        u = get_or_create_session_user()
        return u if u and u.is_admin else None

    from flask import request

    @app.get("/become-admin")
    def become_admin():
        """Zet de huidige sessie-user als admin (super simpel voor lokaal testen)."""
        u = get_or_create_session_user()
        u.is_admin = True
        db.session.commit()
        flash("Je bent nu admin (sessie-user).", "success")
        return redirect(url_for("editions"))


    # ✅ homepage endpoint heet 'editions'
    @app.get("/", endpoint="editions")
    def editions():
        return render_template("editions.html")

    @app.get("/health")
    def health():
        try:
            db.session.execute(text("select 1"))
            return {"status": "ok"}, 200
        except Exception as e:
            return {"status": "error", "detail": str(e)}, 500

    @app.route("/suggest", methods=["GET", "POST"])
    def suggest():
        if request.method == "POST":
            artist_name = request.form.get("artist_name", "").strip()
            if not artist_name:
                flash("Geef een artiestnaam op.", "warning")
                return redirect(url_for("suggest"))
            a = Artists(Artist_name=artist_name)
            db.session.add(a); db.session.commit()
            s = SuggestionFeedback(artist_id=a.id)
            db.session.add(s); db.session.commit()
            flash("Bedankt voor je suggestie!", "success")
            return redirect(url_for("editions"))
        return render_template("suggest.html")
    
    @app.get("/admin/seed-edition-2026")
    def seed_edition_2026():
        admin = require_admin()
        if not admin:
            flash("Alleen voor beheerders.", "warning")
            return redirect(url_for("editions"))

        # Bestaat er al eentje met Name='2026'? Zo ja, niets doen.
        existing = FestivalEdition.query.filter_by(Name="2026").first()
        if existing:
            flash("Editie 2026 bestond al.", "info")
            return redirect(url_for("editions"))

        ed = FestivalEdition(
            Name="2026",
            Location="Dendermonde",
            Start_date=date(2026, 8, 21),
            End_date=date(2026, 8, 24),
        )
        db.session.add(ed); db.session.commit()
        flash("Editie 2026 aangemaakt!", "success")
        return redirect(url_for("editions"))
    from flask import request, redirect, url_for, flash, render_template

    @app.route("/register", methods=["GET", "POST"])
    def register():
        # Als al ingelogd: direct naar home
        if get_session_user():
            flash("Je bent al aangemeld.", "info")
            return redirect(url_for("editions"))

        if request.method == "POST":
            email = (request.form.get("email") or "").strip()
            # 1) als email is opgegeven en bestaat al: hergebruik die
            user = None
            if email:
                user = User.query.filter_by(email=email).first()
            # 2) geen bestaande user? maak er één (email mag leeg)
            if not user:
                user = User(email=email or None)
                db.session.add(user)
                db.session.commit()
            # 3) login in sessie
            login_user(user)
            flash(f"Aangemeld als user #{user.id}", "success")
            return redirect(url_for("editions"))

        # GET: toon formulier
        return render_template("register.html")

    @app.get("/logout")
    def logout():
        if get_session_user():
            logout_user()
            flash("Je bent afgemeld.", "info")
        return redirect(url_for("editions"))

    return app
