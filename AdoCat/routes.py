from functools import wraps
from flask import Flask, render_template, request, redirect, flash, session, url_for
from main import app, db, Usuario, Gato




#rota da pagina "home"



@app.route('/')
def default():
    return redirect('/home')
    


@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/login')

    nome_usuario = session.get('user_name')
    lista_gatos = Gato.query.order_by(Gato.id_gato)


    return render_template("homepage.html",
                           usuario = nome_usuario,
                           gatos_listados = lista_gatos,
                           nomeGato = Gato.nome_gato)


@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/logar', methods=['POST'])
def logar():
    email = request.form['email']
    senha = request.form['senha']
    
    usuario = Usuario.query.filter_by(email_user=email).first()
    
    if usuario and usuario.senha_user == senha:
        session['user_id'] = usuario.id_user
        session['user_name'] = usuario.nome_user
        return redirect('/home')
    else:
        return render_template("login.html", 
                               menssagem = "Credenciais inválidas!!!")
    

@app.route('/logout')
def logout():
    session.clear()  # Remove todos os dados da sessão
    return redirect('/')





@app.route('/cadastro')
def cadastro():
    return render_template("cadastro.html")

@app.route("/cadastrar", methods=['POST',])
def adiciona_registro():
    try:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha'] 

        new_user = Usuario(nome_user=nome, email_user=email, senha_user=senha)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')

    except Exception as e:
        db.session.rollback()  # Reverta a sessão em caso de erro
        return str(e), 500  # Retorne o erro