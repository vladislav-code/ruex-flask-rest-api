import shutil
from datetime import datetime, timedelta

from sqlalchemy import event

from main import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# вынести создание бд в этот модуль

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

    orders = db.relationship('Order', backref='client', lazy=True, cascade='all, delete-orphan')


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.String(80), nullable=False)
    # services = db.relationship('Service', secondary='order_service', backref='orders')

    documents = db.relationship('Document', backref='order', lazy=True, cascade='all, delete-orphan')


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    direction = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(150), nullable=False)
    details = db.Column(db.String(50))
    specific = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False)
    execution_time = db.Column(db.String(20))

    orders = db.relationship('Order', backref='service', lazy=True, cascade='all, delete-orphan')


class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    def delete(self):
        # Удаление файла с диска
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)
        # Удаление записи из базы данных
        db.session.delete(self)
        db.session.commit()


@event.listens_for(Document, 'before_delete')
def delete_document_files(mapper, connection, target):
    try:
        order_directory = os.path.dirname(target.file_path)
        if os.path.isdir(order_directory):
            # Удаляем директорию и все ее содержимое
            shutil.rmtree(order_directory)
    except Exception as e:
        print(f"Error deleting directory: {e}")


# Создание контекста приложения
# with app.app_context():
#     # Создание таблиц в базе данных
#     db.create_all()


# class Review(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     client_name = db.Column(db.String(255), nullable=False)
#     date = db.Column(db.DateTime, nullable=False)
