from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    department = db.Column(db.String(64), nullable=False)
    privilege = db.Column(db.Integer, default=0)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class ServiceCall(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)
    completion_deletion_date = db.Column(db.DateTime, nullable=True)
    department = db.Column(db.String(64), nullable=False)
    requesting_user = db.Column(db.String(64), nullable=False)
    completing_deleting_user = db.Column(db.String(64), nullable=True)
    urgency = db.Column(db.String(10), nullable=False)
    call_type = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
