# модуль, в котором описаны функции и соответвующие им url
# роутинг
from flask import jsonify, request, render_template
from sqlalchemy import func

from main import app
import funcs
from flask_jwt_extended import JWTManager, jwt_required
# from flask_mail import Message
from utils import admin_required, confirmed_required
# TODO добавить требование подтвержденного пользователя
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

jwt = JWTManager(app)
bcrypt = Bcrypt(app)


@app.route('/api/send_mail', methods=['POST'])
def send_email():
    return funcs.send_mail()


@app.route('/api/login', methods=['POST'])
def login():
    return funcs.login()


@app.route('/api/user', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_user():
    return funcs.handle_user()


@app.route('/api/services', methods=['GET'])
def get_services():
    return funcs.get_services()


# TODO нужен ли /user/ в запросах пользователя
@app.route('/api/user/orders', methods=['GET'])
@jwt_required()
@confirmed_required
def get_user_orders():
    return funcs.get_user_orders()


@app.route('/api/user/orders', methods=['POST'])
@jwt_required()
@confirmed_required
def create_order():
    return funcs.create_order()


@app.route('/api/admin/orders', methods=['GET'])
@jwt_required()
@confirmed_required
@admin_required
def get_admin_orders():
    return funcs.get_admin_orders()


@app.route("/api/admin/order/<int:order_id>", methods=['PUT'])
@jwt_required()
@confirmed_required
@admin_required
def admin_update_order(order_id):
    return funcs.update_order(order_id)


@app.route("/api/admin/order/<int:order_id>", methods=['DELETE'])
@jwt_required()
@confirmed_required
@admin_required
def admin_delete_order(order_id):
    return funcs.delete_order(order_id)


@app.route("/api/admin/service/<int:service_id>", methods=['PUT', 'DELETE'])
@jwt_required()
@confirmed_required
@admin_required
def admin_service(service_id):
    return funcs.admin_service(service_id)


# TODO время действия ссылки подтверждения
@app.route('/api/confirm_email/<token>')
def confirm_email(token):
    return funcs.confirm_email(token)


@app.route('/api/register', methods=['POST'])
def register():
    return funcs.register()


@app.route('/api/reset-password', methods=['POST'])  # добавить jwt
def reset_password():
    return funcs.reset_password()


# TODO проверить
@app.route('/api/reset-password/<reset_token>', methods=['POST'])
def reset_password_token(reset_token):
    return reset_password_token(reset_token)
