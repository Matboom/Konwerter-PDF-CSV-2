from flask import Flask

app = Flask(__name__)

# Importuj konfigurację
app.config.from_pyfile('config.py')

from app import routes
