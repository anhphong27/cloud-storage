from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import os

### Create app------------------------------------------------------------------------------------------
app = Flask(__name__)

### Secret Key------------------------------------------------------------------------------------------
app.secret_key = 'asdasdasd1h23j123jsadsuidhaisudhaisudh@W@#'

### Domain------------------------------------------------------------------------------------------
app.config["DOMAIN"] = os.getenv("DOMAIN")

### Database------------------------------------------------------------------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://admin:%s@test-db.c607f6oqfbba.us-east-1.rds.amazonaws.com/storage?charset=utf8mb4" % quote('Phong.2709')
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
