from estudo import db
from datetime import datetime

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.now())
    nome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    mensagem = db.Column(db.String, nullable=False)
    assunto = db.Column(db.String, nullable=False)
    respondido = db.Column(db.Integer, default=0)


