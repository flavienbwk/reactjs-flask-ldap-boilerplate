from datetime import datetime

from sqlalchemy import func

from ..app import database


db = database.getDatabase()

class User(db.Model):
    __tablename__ = 'User'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ids = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now())
    
    def __repr__(self):
        return "<User(username='{}', first_name='{}', last_name='{}')>".format(
            self.username, 
            self.first_name, 
            self.last_name
        )