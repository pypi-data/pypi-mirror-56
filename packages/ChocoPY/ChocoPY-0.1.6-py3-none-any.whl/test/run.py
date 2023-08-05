from flask import Flask
from chocopy import ChocoPY

app = Flask(__name__)

ChocoPY(app)

app.run()