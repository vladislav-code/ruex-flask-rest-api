# переименовать в ruex ??
# модуль flask приложения, должен содержать app = Flask(__name__)
# добавить logger
# логгирование
from flask import Flask
import os
# from flask_mail import Mail
# from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required
# в модуле tests проверка на name error локально
# невыполняющиеся импорты
# желательно проверить все IF


from config import DevelopmentConfig
# from models import Order, Service, order_service

app = Flask(__name__) #
# mail = Mail(app)
app.config.from_object(DevelopmentConfig) #

# ruex_db = SqliteDatabase("ruex.db") for pewee
# выбрать бД и создать ее
# pewee or alchemy ???


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # change to ruex.db

import views
