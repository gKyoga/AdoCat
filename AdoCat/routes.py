from functools import wraps
from flask import Flask, render_template, request, redirect, flash, session, url_for
from main import app, db, Usuario, Gato
import os
from werkzeug.utils import secure_filename


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'assets')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



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
    session.clear()  
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
        db.session.rollback()  
        return str(e), 500  
    


@app.route('/CadastroGato')
def CadastroGato():
    return render_template( "cadastroGato.html")


@app.route('/CadastrarGato', methods=['POST'])
def AdicionaGato():
    try:
        nome = request.form['NomeGato']
        idade = int(request.form['IdadeGato'].replace("Anos", "").strip())
        sexo = request.form['SexoGato']
        vacina = True if request.form.get('VacinaGato') else False
        descricao = request.form['DescricaoGato']
        usuario = session.get('user_id')
        imagem = request.files.get('ImagemGato')
        
        nome_arquivo = None
        if imagem and allowed_file(imagem.filename):
            nome_arquivo = secure_filename(imagem.filename)
            caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
            imagem.save(caminho_arquivo)

        
        new_gato = Gato(
            nome_gato=nome,
            idade_gato=idade,
            sexo_gato=sexo,
            descricao_gato=descricao,
            vacina_gato=vacina,
            user_id=usuario,
            foto_gato=nome_arquivo
        )

        db.session.add(new_gato)
        db.session.commit()
        return redirect('/home')

    except Exception as e:
        db.session.rollback()
        return f"Erro ao cadastrar o gato: {str(e)}", 500




@app.route('/UpdateGato/<int:gato_id>', methods=['GET', 'POST'])
def UpdateGato(gato_id):

    gato = Gato.query.get(gato_id)
    
    if gato:
        return render_template("updateGato.html", gato=gato)
    else:
        return "Gato não encontrado", 404
    

@app.route('/AtualizarGato/<int:gato_id>', methods=['GET', 'POST'])
def AtualizarGato(gato_id):
    gato = Gato.query.get(gato_id)
    
    if gato:
        if request.method == 'POST':
            gato.nome_gato = request.form['NomeGato']
            gato.idade_gato = int(request.form['IdadeGato'].replace("Anos", "").strip())
            gato.sexo_gato = request.form['SexoGato']
            gato.descricao_gato = request.form['DescricaoGato']
            gato.vacina_gato = True if request.form.get('VacinaGato') else False
            
            imagem = request.files.get('ImagemGato')
            if imagem and allowed_file(imagem.filename):
                nome_arquivo = secure_filename(imagem.filename)
                caminho_arquivo = os.path.join(UPLOAD_FOLDER, nome_arquivo)
                imagem.save(caminho_arquivo)
                gato.foto_gato = nome_arquivo
            
            db.session.commit()
            return redirect('/home')
        
        return render_template("updateGato.html", gato=gato)
    
    return "Gato não encontrado", 404


@app.route('/DeletarGato/<int:gato_id>', methods=['GET'])
def DeletarGato(gato_id):
    gato = Gato.query.get(gato_id)
    
    if gato:
        db.session.delete(gato)
        db.session.commit()
        return redirect('/home')
    
    return "Gato não encontrado", 404

