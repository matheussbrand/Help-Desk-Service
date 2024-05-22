from app import app, db
from models import User, ServiceCall

with app.app_context():
    db.create_all()

    # Optionally, create an initial admin user
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            name="Admin User",
            role="Administrator",
            department="IT",
            privilege=2,
        )
        admin.set_password("adminpassword")
        db.session.add(admin)
        db.session.commit()
