from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, static_folder='static')


app.secret_key = 'ninacomemuito'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}{versao}'.format(
        SGBD = 'mysql+pymysql',
        senha = 'teste',
        usuario = 'teste',
        servidor = '127.0.0.1',
        database = 'db_adocat',
        versao = '?charset=utf8mb4',
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  


db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'tbl_users'
    
    id_user = db.Column(db.Integer, primary_key=True)
    nome_user = db.Column(db.String(100), nullable=False)
    email_user = db.Column(db.String(100), unique=True, nullable=False)
    senha_user = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Gato(db.Model):
    __tablename__ = 'tbl_gatos'
    
    id_gato = db.Column(db.Integer, primary_key=True)
    nome_gato = db.Column(db.String(100), nullable=False)
    idade_gato = db.Column(db.String(15), nullable=False)
    sexo_gato = db.Column(db.String(6), nullable=False)
    vacina_gato = db.Column(db.Boolean, nullable=False, default=False)
    descricao_gato = db.Column(db.Text)
    foto_gato = db.Column(db.String(255))
    status_gato = db.Column(db.String(50), nullable=False, default='Disponível')
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_users.id_user'))
    data_cadastro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    usuario = db.relationship('Usuario', backref=db.backref('gatos', lazy=True))

#importação das rotas para o progama principal
from routes import *


if __name__ == '__main__':
    app.run(debug=True)
