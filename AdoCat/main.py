from flask import Flask
from flask import render_template

app = Flask(__name__)


#importação das rotas para o progama principal
from routes import *


if __name__ == '__main__':
    app.run(debug=True)
