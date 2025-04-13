from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from dotenv import load_dotenv
import os

app = Flask(__name__)

app.secret_key = 'asdasdasd1h23j123jsadsuidhaisudhaisudh@W@#'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/storage?charset=utf8mb4" % quote('1234')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['UPLOAD_FOLDER'] = 'data'

app.config['STRIPE_API_KEY_PRIVATE']= os.getenv("STRIPE_API_KEY_PRIVATE")
app.config['STRIPE_API_KEY_PUBLIC']= os.getenv("STRiPE_API_KEY_PUBLIC")
db = SQLAlchemy(app)

login_manager = LoginManager(app)
