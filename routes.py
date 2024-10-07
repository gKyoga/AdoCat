from main import app, render_template


#rota da pagina "home"
@app.route('/')
def home():
    return render_template("homepage.html")