#inicializa la app
from flask import Flask 

app = Flask(__name__)

#establecemos llave

app.secret_key = "Mi llave secreta"