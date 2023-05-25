from datetime import datetime
from main import app
from flask_sqlalchemy import SQLAlchemy

# вынести создание бд в этот модуль

db = SQLAlchemy(app)


# from werkzeug.security import generate_password_hash, check_password_hash


# Пользователи
# Услуги
# Админ
# Заказы
# Объекты?
# Сотрудники?

# хранение файлов
# Отзывы?

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True) # unique ????
    username = db.Column(db.String(80), unique=True, nullable=False) # необходимость unique
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=True) # необходимость unique
    is_admin = db.Column(db.Boolean, default=False)
    email_confirmed = db.Column(db.Boolean, default=False)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(80), nullable=False)
    # services = db.relationship('Service', secondary='order_service', backref='orders')


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    direction = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(150), nullable=False)
    details = db.Column(db.String(50))
    specific = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    execution_time = db.Column(db.String(20))


# Создание контекста приложения
with app.app_context():
    # Создание таблиц в базе данных
    db.create_all()


# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     client_name = db.Column(db.String(255), nullable=False)
#     date = db.Column(db.DateTime, nullable=False)
