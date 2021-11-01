from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import Column, Boolean, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from .settings import DATABASE, HOST, DB_PASSWORD, DB_USER, DB_NAME
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


def setup_db(app):
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"{DATABASE}://{DB_USER}:{DB_PASSWORD}@{HOST}/{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String(150), nullable=False)
    password = Column(String)
    role = Column(String)

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def __repr__(self):
        return f"<User id:{self.id} username:{self.username}>"

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            "name": self.username,
            "id": self.id,
            "email": self.email,
            "role": self.role,
        }


class Course(db.Model):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    title = Column(String)
    filename = Column(String)

    def __init__(self, content, title, filename):
        self.content = content
        self.title = title
        self.filename = filename

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            "title": self.title,
            "id": self.id,
            "content": self.content,
        }

    def format_short(self):
        return {
            "title": self.title,
            "id": self.id,
        }
