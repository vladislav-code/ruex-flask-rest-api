# утилитные функции из различных модулей
# если в заголовках закодированное здесь можно осуществлять декодирование
# функции которые могут вызываться в разных частях программы
# функции, скопированные из интернета, проверка валидности

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


def confirmed_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = db.session.query(User).filter_by(id=user_id).first()

        if user is None:
            return jsonify({"msg": "User not found"}), 404
        elif not user.email_confirmed:
            return jsonify({"msg": "Admin access required"}), 403

        return f(*args, **kwargs)
    return decorated_function


ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
