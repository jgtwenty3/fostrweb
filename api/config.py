import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session  # Import Flask-Session here
from sqlalchemy import MetaData
from flask_socketio import SocketIO
import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'  # Use the 'filesystem' type for simplicity
# app.config['SESSION_TYPE'] = 'redis'

app.config['SESSION_TYPE'] = 'filesystem'  # Using filesystem storage
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'your_prefix'
app.config['SESSION_COOKIE_SAMESITE'] = 'None' 
app.config['SESSION_COOKIE_SECURE'] = True  # This must be set
# app.config['SESSION_COOKIE_HTTPONLY'] = True  # Security best practice
# app.config['SESSION_COOKIE_PATH'] = '/'  # Ensure the cookie is sent on all routes

# Initialize Flask-Session after setting configs
Session(app)





# Define metadata, instantiate db
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})



db = SQLAlchemy(metadata=metadata)
migrate = Migrate(app, db)
db.init_app(app)

# Instantiate REST API
api = Api(app)

# Instantiate CORS
CORS(app, supports_credentials=True,origins=["http://localhost:3000"])


