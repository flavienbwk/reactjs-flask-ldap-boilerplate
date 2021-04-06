from ..model.User import User

from ..app import database


db = database.getDatabase()

class Token(db.Model):
    __tablename__ = 'Token'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ids = db.Column(db.String(64), unique=True, nullable=False)
    ip = db.Column(db.String(64), nullable=True)
    token = db.Column(db.Text, nullable=False)
    User_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    ut_created_at = db.Column(db.Integer, nullable=False)
    ut_expires_at = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return "<Token(id='{}', ids='{}')>".format(
            self.id, 
            self.ids
        )