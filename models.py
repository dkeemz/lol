from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(120), nullable=True)
    lga = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(120), nullable=False)
    contractor = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    latLng = db.Column(db.PickleType, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    images = db.relationship('Image', backref='project', lazy=True)
    videos = db.relationship('Video', backref='project', lazy=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(120), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
