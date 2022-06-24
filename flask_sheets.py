from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_fontawesome import FontAwesome
from flask_migrate import Migrate




app = Flask(__name__, static_folder='sources/static', template_folder='sources/templates')

db = SQLAlchemy(app)
db_session = db.session


@app.route('/')
def spreadsheet():
    return render_template('index.html')

app.run(debug=True)