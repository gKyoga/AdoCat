from main import app, render_template,Gato


#rota da pagina "home"
@app.route('/')
def home():
    lista_gatos = Gato.query.order_by(Gato.id_gato)

    return render_template("homepage.html",
                           gatos_listados = lista_gatos,
                           nomeGato = Gato.nome_gato)