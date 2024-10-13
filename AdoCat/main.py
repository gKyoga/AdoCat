from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:toor@1234@localhost/db_adocat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'tbl_users'
    id_user = db.Column(db.Integer, primary_key=True)
    nome_user = db.Column(db.String(100), nullable=False)
    email_user = db.Column(db.String(100), unique=True, nullable=False)
    senha_user = db.Column(db.String(255), nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

class Gato(db.Model):
    __tablename__ = 'tbl_gatos'
    id_gato = db.Column(db.Integer, primary_key=True)
    nome_gato = db.Column(db.String(100), nullable=False)
    idade_gato = db.Column(db.Integer, nullable=False)
    descricao_gato = db.Column(db.Text)
    foto_gato = db.Column(db.String(255))
    status_gato = db.Column(db.String(50), nullable=False, default='Disponível')
    user_id = db.Column(db.Integer, db.ForeignKey('tbl_users.id_user'))
    data_cadastro = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

#importação das rotas para o progama principal
from routes import *


if __name__ == '__main__':
    app.run(debug=True)
