# модуль, в котором описаны функции и соответвующие им url
# роутинг
from flask import jsonify, request, render_template
from sqlalchemy import func

from main import app
import funcs
from models import User, Service, Order, Document, db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
# from flask_mail import Message
from utils import admin_required, confirmed_required
# TODO добавить требование подтвержденного пользователя
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# @app.route('/services', methods=['GET'])
# def get_services():
#     services = Service.query.all()
#     return jsonify([{'id': s.id, 'name': s.name, 'description': s.description} for s in services])


# @app.route('/services')
# def get_services():
#     services = Service.query.all()
#     result = []
#
#     for service in services:
#         if isinstance(service, EvaluationService):
#             result.append({
#                 'id': service.id,
#                 'name': service.name,
#                 'type': service.type,
#                 'description': service.description,
#                 'object_type': service.object_type,
#                 'evaluation_goal': service.evaluation_goal,
#             })
#         elif isinstance(service, OtherService):
#             result.append({
#                 'id': service.id,
#                 'name': service.name,
#                 'type': service.type,
#                 'description': service.description,
#                 # другие поля для этого типа услуги
#                 # ...
#             })
#         else:
#             result.append({
#                 'id': service.id,
#                 'name': service.name,
#                 'type': service.type,
#                 'description': service.description,
#             })
#
#     return jsonify(result)


# TODO хэширование пароля
# @app.route('/login', methods=['POST'])
# def login():
#     # username = request.json.get('username', None)
#     # password = request.json.get('password', None)
#     #
#     # user = User.query.filter_by(username=username).first()
#     # if not user:
#     #     return jsonify({'msg': 'Invalid username or password'}), 401
#     #
#     # if not password:
#     #     return jsonify({'msg': 'Password is missing'}), 400
#     #
#     # if password != user.password:
#     #     return jsonify({'msg': 'Invalid username or password'}), 401
#
#     username = request.json.get('username', None)
#     password = request.json.get('password', None)
#
#     user = User.query.filter_by(username=username).first()
#     if user is None or password != user.password_hash:
#         return jsonify({'msg': 'Invalid username or password'}), 401
#
#     if not username or not password:
#         return jsonify({'msg': 'Username or password is missing'}), 400
#
#     # if username != 'admin' or password != 'admin':
#     #     return jsonify({'msg': 'Invalid username or password'}), 401
#
#     access_token = create_access_token(identity=username)
#     return jsonify({'access_token': access_token}), 200


# @app.route('/register', methods=['POST'])
# def register():
#     username = request.json.get('username', None)
#     password_hash = request.json.get('password', None)  # добавить хэш функцию
#     email = request.json.get('email', None)
#
#     if not username or not password_hash:
#         return jsonify({'msg': 'Username or password is missing'}), 400
#
#     # проверка, существует ли пользователь
#     user = User.query.filter_by(username=username).first()
#     if user:
#         return jsonify({'msg': 'User already exists'}), 400
#
#
#     # Получаем первый свободный id
#     first_free_id = db.session.query(func.min(User.id + 1)). \
#         filter(~User.id.in_(db.session.query(User.id)))
#     new_user = User(id=first_free_id, username=username, password_hash=password_hash, email=email)
#
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User created successfully'}), 201


# подтверждение регистрации
from flask_jwt_extended import get_jwt_identity, jwt_required


# @app.route('/confirm-registration/<token>', methods=['GET'])
# @jwt_required()
# def confirm_registration(token):
#     try:
#         # Декодировать токен
#         decoded_token = decode_token(token)
#         user_id = decoded_token['identity']
#
#         # Пометить пользователя как подтвержденного в базе данных
#         confirm_user(user_id)
#
#         return {'message': 'Регистрация подтверждена успешно.'}, 200
#     except:
#         return {'message': 'Ошибка при подтверждении регистрации.'}, 400


@app.route('/api/send_mail', methods=['POST'])
def send_email():
    return funcs.send_mail()


# TODO подтверждение по почте? почтовая рассылка
# @app.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
#     new_user = User(
#         username=data['username'],
#         password_hash=hashed_password,
#         email=data['email'],
#         phone_number=data['phone_number'],
#         is_admin=data.get('is_admin', False)
#     )
#     db.session.add(new_user)
#     try:
#         db.session.commit()
#     except IntegrityError:  # все поля уникальны
#         return jsonify(message="User with that username or email already exists"), 400
#     return jsonify(message="User registered successfully"), 201


@app.route('/api/login', methods=['POST'])
def login():
    return funcs.login()


@app.route('/api/user', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_user():
    return funcs.handle_user()


# @app.route('/service/<int:service_id>', methods=['GET'])
# def get_service(service_id):
#     service = Service.query.get(service_id)
#
#     if service is None:
#         return jsonify(message="Service not found"), 404
#
#     service_data = {
#         'id': service.id,
#         'name': service.name,
#         'type': service.type,
#     }
#
#     if isinstance(service, EvaluationService):
#         service_data.update({
#             'object_type': service.object_type,
#             'evaluation_goal': service.evaluation_goal,
#             'price': service.price,
#             'execution_time': service.execution_time,
#         })
#     elif isinstance(service, ExpertiseService):
#         service_data.update({
#             'object_space': service.object_space,
#             'evaluation_goal': service.evaluation_goal,
#             'price': service.price,
#             'execution_time': service.execution_time,
#         })
#
#     return jsonify(service_data), 200


@app.route('/api/services', methods=['GET'])
def get_services():
    return funcs.get_services()


# TODO нужен ли /user/ в запросах пользователя
@app.route('/api/user/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    return funcs.get_user_orders()


# @app.route('/api/user/orders', methods=['POST'])
# @jwt_required()
# def create_order():
#     return funcs.create_order()


@app.route('/api/admin/orders', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_orders():
    return funcs.get_admin_orders()


# @app.route('/payment', methods=['POST'])
# def payment():
#
#     return #jsonify(services_data), 200
#
#
# @app.route('/upload', methods=['POST'])
# @jwt_required()
# def upload():
#
#
# @app.route("/admin/order/<int:order_id>", methods=['PUT', 'DELETE'])
# @jwt_required()
# @admin_required()
# def admin_order():
#
#
@app.route("/api/admin/service/<int:service_id>", methods=['PUT', 'DELETE'])
@jwt_required()
@admin_required
def admin_service(service_id):
    return funcs.admin_service()


# TODO время действия ссылки подтверждения
@app.route('/api/confirm_email/<token>')
def confirm_email(token):
    return funcs.confirm_email(token)


@app.route('/api/register', methods=['POST'])
def register():
    return funcs.register()


# @app.route('/reset-password', methods=['POST'])
# def reset_password():
#     email = request.form['email']
#     token = serializer.dumps(email, salt='password-reset-salt')
#
#     msg = MIMEMultipart()
#     msg['From'] = "your_email@example.com"
#     msg['To'] = email
#     msg['Subject'] = 'Password Reset Request'
#
#     link = url_for('reset_password_token', token=token, _external=True)
#
#     msg.attach(MIMEText('Follow this link to reset your password: {}'.format(link), 'plain'))
#
#     try:
#         server = smtplib.SMTP(smtp_server,port)
#         server.ehlo() # Can be omitted
#         server.starttls() # Secure the connection
#         server.ehlo() # Can be omitted
#         server.login(username, password)
#         server.sendmail(msg['From'], msg['To'], msg.as_string())
#         server.close()
#
#         print('Email sent!')
#     except Exception as e:
#         # Print any error messages to stdout
#         print(e)
#
#     return 'Email sent!'
#
#
# @app.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password_token(token):
#     try:
#         email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
#     except:
#         return 'The password reset link is invalid or has expired.'
#
#     # Здесь вы можете использовать 'email' для получения пользователя из базы данных
#     # и обновления их пароля
#
#     return 'Password has been reset!'


@app.route('/api/reset-password', methods=['POST'])  # добавить jwt
@jwt_required()
def reset_password():
    return funcs.reset_password()


# @app.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password_token(token):
#     try:
#         email = decode_token(token)
#     except:
#         return 'The password reset link is invalid or has expired.'
#
#     # Здесь вы можете использовать 'email' для получения пользователя из базы данных
#     # и обновления их пароля
#
#     return 'Password has been reset!'

# TODO проверить
@app.route('/api/reset-password/<reset_token>', methods=['POST'])
def reset_password_token(reset_token):
    return reset_password_token(reset_token)


@app.route('/api/create_order', methods=['POST'])
@jwt_required()
def create_order():
    return funcs.create_order()


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')
