from flask import Flask, request, url_for
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_mail import Mail
from flasgger import Swagger

from .logger import Logger
from .config import config


# General flask app
app = Flask(__name__)

# SQLAlchemy
db = SQLAlchemy()

# API
marshmallow = Marshmallow()

# mail
mail = Mail()

# Security
security = Security()

# Logging
logger = Logger()

# Swagger
swag = Swagger()
