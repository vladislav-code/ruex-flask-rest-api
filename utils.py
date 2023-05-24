# утилитные функции из различных модулей
# если в заголовках закодированное здесь можно осуществлять декодирование
# функции которые могут вызываться в разных частях программы
# функции, скопированные из интернета, проверка валидности
import hashlib
import binascii
import os

from flask import jsonify

from models import db, User
from functools import wraps

from flask_jwt_extended import get_jwt_identity


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()

        if user is None:
            return jsonify({"msg": "User not found"}), 404
        elif not user.is_admin:
            return jsonify({"msg": "Admin access required"}), 403

        return f(*args, **kwargs)
    return decorated_function


def hash_password_pbkdf2(password, salt=None):
    if not salt:
        # Генерация случайной "соли" если её нет
        salt = os.urandom(16)

    # Применение PBKDF2 алгоритма для хеширования пароля с "солью"
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)

    # Конвертация бинарного хеша и "соли" в строковое представление
    salt_str = binascii.hexlify(salt).decode()
    password_hash_str = binascii.hexlify(password_hash).decode()

    return f"{salt_str}:{password_hash_str}"