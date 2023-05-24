# модуль, в котором описаны функции и соответвующие им url
# роутинг
from flask import jsonify, request
from sqlalchemy import func
from main import app  # , mail
import funcs
from models import User, Service, Order, db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
# from flask_mail import Message
from utils import admin_required

from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

jwt = JWTManager(app)
bcrypt = Bcrypt(app)


@app.route('/api/orders', methods=['GET'])
@jwt_required()  # Декоратор, требующий авторизации по JWT токену для доступа к эндпоинту
def get_orders():
    orders = Order.query.all()
    return jsonify(
        [{'id': o.id, 'customer_name': o.customer_name, 'custome_email': o.customer_email, 'order_date': o.order_date}
         for o in orders])


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
from flask_jwt_extended import decode_token, get_jwt_identity, jwt_required


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


# TODO восстановление пароля по почте
@app.route('/api/login', methods=['POST'])
# добавить проверки данных
# проверка наличия данных
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid email or password"), 401


@app.route('/api/user', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def handle_user():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)

    # if not current_user.is_admin:
    #     return jsonify(message="Not authorized"), 403

    user = User.query.get(user_id)

    if request.method == 'GET':
        return jsonify(username=user.username, email=user.email, phone_number=user.phone_number,
                       is_admin=user.is_admin), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if 'username' in data:
            user.username = data['username']
        if 'password' in data:
            user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        if 'email' in data:
            user.email = data['email']
        if 'phone_number' in data:
            user.phone_number = data['phone_number']
        try:
            db.session.commit()
        except IntegrityError:
            return jsonify(message="Something wrong"), 400  # ошибка с бд
        return jsonify(message="User updated successfully"), 200
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify(message="User deleted successfully"), 200


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
    services = Service.query.all()
    services_list = []
    for service in services:
        service_data = {
            'direction': service.direction,
            'type': service.type,
            'details': service.details,
            'specific': service.specific,
            'price': service.price,
            'execution_time': service.execution_time
        }
        services_list.append(service_data)
    return jsonify(services_list), 200


# TODO нужен ли /user/ в запросах пользователя
@app.route('/api/user/orders', methods=['GET'])
@jwt_required()
def get_user_orders():
    # user_id = get_jwt_identity()
    # # if current_user_id != user_id:
    # #     return jsonify({"msg": "Unauthorized access"}), 403
    #
    # orders = Order.query.filter_by(client_id=user_id).all()
    # orders_list = []
    # for order in orders:
    #     order_data = {
    #         'id': order.id,
    #         'client_id': order.client_id,
    #         'service_id': order.service_id,
    #         'order_date': order.order_date,
    #         'status': order.status
    #     }
    #     orders_list.append(order_data)
    # return jsonify(orders_list), 200
    user_id = get_jwt_identity()
    orders = db.session.query(Order, Service).join(Service, Order.service_id == Service.id).filter(Order.client_id == user_id).all()
    orders_list = []
    for order, service in orders:
        order_data = {
            'id': order.id, ###
            'client_id': order.client_id, ###
            'service': {
                'id': service.id, ###
                'direction': service.direction,
                'type': service.type,
                'details': service.details,
                'specific': service.specific,
                'price': service.price,
                'execution_time': service.execution_time
            },
            'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'status': order.status
        }
        orders_list.append(order_data)
    return jsonify(orders_list), 200


@app.route('/api/user/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()

    if 'direction' not in data or 'type' not in data or 'details' not in data or 'specific' not in data or 'price' not in data or 'execution_time' not in data:
        return jsonify({"msg": "Missing service parameters"}), 400

    service = Service.query.filter_by(direction=data['direction'], type=data['type'], details=data['details'],
                                      specific=data['specific'], price=data['price'],
                                      execution_time=data['execution_time']).first()
    if service is None:
        return jsonify({"msg": "Service not found"}), 404

    new_order = Order(
        client_id=user_id,
        service_id=service.id,
        status='Принят'
    )

    db.session.add(new_order)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        return jsonify({"msg": "Database error occurred. " + str(e)}), 500

    return jsonify({"msg": "Order created successfully!"}), 201


@app.route('/api/admin/orders', methods=['GET'])
@jwt_required()
@admin_required
def get_admin_orders():

    orders = Order.query.all()
    orders_list = []
    for order in orders:
        order_data = {
            'id': order.id,
            'client_id': order.client_id,
            'service_id': order.service_id,
            'order_date': order.order_date.strftime('%Y-%m-%d %H:%M:%S'), # проверить как лучше в сравнии выше
            'status': order.status
        }
        orders_list.append(order_data)
    return jsonify(orders_list), 200


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
    try:
        service = Service.query.get(service_id)

        if service is None:
            return jsonify({"error": "Service not found"}), 404

        if request.method == 'PUT':
            # Update the service record
            # переделать для нового формата услуг
            service.name = request.json.get('name', service.name)
            service.type = request.json.get('type', service.type)

        elif request.method == 'DELETE':
            # Delete the service record
            db.session.delete(service)

        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

    if request.method == 'DELETE':
        return jsonify(message="Service deleted successfully"), 200
    else:
        return jsonify(service.to_dict())  # Assuming Service model has a to_dict() method


# TODO время действия ссылки подтверждения
@app.route('/api/confirm_email/<token>')
def confirm_email(token):
    # email = get_jwt_identity()

    try:
        # Мы не используем здесь jwt_required, так как токен передается в URL, а не в заголовке Authorization.
        decoded_token = decode_token(token, allow_expired=True)
        email = decoded_token['sub'] # get_jwt_identity?
    except Exception as e: # для чего exception ?
        # Ошибка будет возникать, если токен недействителен или истек.
        return jsonify(message="The confirmation link is invalid or has expired."), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(message="User does not exist."), 400

    if user.email_confirmed:
        return jsonify(message="User already confirmed."), 200

    user.email_confirmed = True
    db.session.commit()

    return jsonify(message="Email confirmed!"), 200


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


# Настройка smtplib
# smtp_server = os.getenv('SMTP_SERVER')
# port = 587  # For starttls
# username = os.getenv('SMTP_USERNAME')
# password = os.getenv('SMTP_PASSWORD')

@app.route('/api/reset-password', methods=['POST']) # добавить jwt
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

# TODO добавить /api/ к роутингу
# TODO проверить
@app.route('/api/reset-password/<reset_token>', methods=['POST'])
def reset_password_token(reset_token):
    try:
        # Мы не используем здесь jwt_required, так как токен передается в URL, а не в заголовке Authorization.
        decoded_token = decode_token(reset_token, allow_expired=True)
        email = decoded_token['sub']  # get_jwt_identity?
    except:
        return jsonify({"msg": "The password reset link is invalid or has expired."}), 400

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    new_password = data.get('password')
    if new_password is None:
        return jsonify({"msg": "No password provided"}), 400

    user.password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        return jsonify({"msg": "Database error occurred. " + str(e)}), 500

    return jsonify({"msg": "Password has been reset!"}), 200