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


# вынести в config
app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER')
app.config['MAIL_PORT'] = os.getenv('SMTP_PORT')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')  # Введите свою почту
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('SMTP_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')  # Введите свой пароль

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # change to ruex.db
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') # change secret !!!!!!!!!!!!!!!!!!!

import views


# jwt = JWTManager(app)
