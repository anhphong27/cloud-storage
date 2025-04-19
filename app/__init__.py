from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv



### Create app------------------------------------------------------------------------------------------
app = Flask(__name__)

load_dotenv()

### Secret Key------------------------------------------------------------------------------------------
app.secret_key = 'asdasdasd1h23j123jsadsuidhaisudhaisudh@W@#'

### Domain------------------------------------------------------------------------------------------
app.config["DOMAIN"] = "127.0.0.1:5000"

### Database------------------------------------------------------------------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1234@localhost/storage?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

### Storage Folder------------------------------------------------------------------------------------------
app.config['UPLOAD_FOLDER'] = 'data'

### Stripe API Key------------------------------------------------------------------------------------------
app.config['STRIPE_API_KEY_PRIVATE'] = os.getenv("STRIPE_API_KEY_PRIVATE")
app.config['STRIPE_API_KEY_PUBLIC'] = os.getenv("STRIPE_API_KEY_PUBLIC")

### Create Database ------------------------------------------------------------------------------------------
db = SQLAlchemy(app)

### Create Flask_Login------------------------------------------------------------------------------------------
login_manager = LoginManager(app)
