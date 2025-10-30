from app import create_app, db
app = create_app()

# Optioneel: voor SQLite eerste keer tabellen maken
# with app.app_context():
#     db.create_all()
