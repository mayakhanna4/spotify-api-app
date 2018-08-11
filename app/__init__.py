from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_navigation import Navigation

app = Flask(__name__)
app.config.from_object(Config)


from app import routes
