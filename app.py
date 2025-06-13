from flask import Flask,  redirect, url_for
from flask_bootstrap import Bootstrap
import os
from logging.config import fileConfig

port = int(os.environ.get('PORT', 3000))

app = Flask(__name__)

app.config.from_object("config")
fileConfig('logging.cfg')
prod = True
Bootstrap(app)
