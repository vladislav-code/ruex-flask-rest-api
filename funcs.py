# модуль с функициями и классами для реализации бизнес логики приложения
# TODO данные почты в отдельный файл
# try catch уязвимых областей
# валидация данных
# from datetime import datetime, timedelta
import datetime
from datetime import datetime as date
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from utils import allowed_file
from flask_mail import Message
from flask import request, url_for, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, decode_token
from main import mail
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from models import User, Service, Order, Document, db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from main import app
import os

# create_user
# confirm_user

bcrypt = Bcrypt(app)

UPLOAD_DIRECTORY = 'files/documents'  # путь к основной директории для хранения файлов
MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB in bytes


def login():
    # добавить проверки данных
    # проверка наличия данных
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        expires = datetime.timedelta(hours=4)
        access_token = create_access_token(identity=user.id, expires_delta=expires)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Invalid email or password"), 401


def handle_user():
    user_id = get_jwt_identity()
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


def get_user_orders():
    user_id = get_jwt_identity()

    orders = db.session.query(Order, Service).join(Service, Order.service_id == Service.id).filter(Order.client_id == user_id).all()
    orders_list = []

    for order, service in orders:
        order_data = {
            'service': {
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


def get_admin_orders():
    orders = db.session.query(Order, Service, User).join(Service, Order.service_id == Service.id).join(User, Order.client_id == User.id).all()
    orders_list = []

    for order, service, user in orders:
        order_data = {
            'order_id': order.id,
            'client': {
                'username': user.username
            },
            'service': {
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


# использовать сервис почтовой рассылки
def send_mail():
    if request.method == 'POST':
        name = request.json['name']
        phone = request.json['phone']
        reason = request.json['reason']
        recipients = ["vladoska75@gmail.com"]

        try:
            msg = Message('New request from website')
            msg.recipients = recipients
            msg.body = f"Имя: {name}\nТелефон: {phone}\nПричина: {reason}"
            mail.send(msg)

            return jsonify({"message": "Mail sent successfully"}), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 500


def register():
    data = request.get_json()

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    expires = datetime.timedelta(days=1)
    token = create_access_token(identity=data['email'], expires_delta=expires)

    new_user = User(
        username=data['username'],
        password_hash=hashed_password,
        email=data['email'],
        phone_number=data['phone_number'],
        is_admin=data.get('is_admin', False),
        email_confirmed=False
    )
    db.session.add(new_user)
    try:
        db.session.commit()
    except IntegrityError: # all fields are unique
        return jsonify(message="Пользователь с таким именем или почтой уже существует"), 400

    confirmation_url = url_for('confirm_email', token=token, _external=True)
    msg = Message('Подтверждение регистрации', sender=app.config['MAIL_USERNAME'], recipients=[data['email']])
    msg.body = 'Пожалуйста, подтвердите свою регистрацию, нажав на следующую ссылку: {0}\n\nЭто сообщение ' \
               'сформировано автоматически, на него не нужно отвечать.'.format(confirmation_url)
    msg.html = '<p>Пожалуйста, подтвердите регистрацию, нажав на следующую ссылку: <a href="{0}">Подтвердить ' \
               'регистрацию</a></p><p><small>Это сообщение сформировано автоматически, на него не нужно ' \
               'отвечать.</small></p>'.format(confirmation_url)

    mail.send(msg)

    return jsonify(message="Письмо с подтверждением отправлено. Пожалуйста, подтвердите свою регистрацию."), 201
    # return jsonify(url_for('confirm_email', token=token, _external=True)), 201
    # return jsonify(message="Confirmation email sent. Please confirm your email."), 201


def reset_password():
    data = request.get_json()
    email = data['email']
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"msg": "Пользователь не найден"}), 404
    expires = datetime.timedelta(hours=24)  # Токен будет действителен 24 часа
    token = create_access_token(identity=email, expires_delta=expires)
    link = url_for('reset_password_token', reset_token=token, _external=True)

    msg = Message('Запрос на сброс пароля',
                  sender=app.config['MAIL_USERNAME'],
                  recipients=[email])

    msg.html = """<html> <body> <h1 style="color: #355C7D; font-family: Arial, sans-serif;">Здравствуйте!</h1> <p 
    style="color: #355C7D; font-family: Arial, sans-serif;"> Мы получили запрос на сброс вашего пароля. Если вы не 
    делали этого запроса, просто проигнорируйте это письмо. В противном случае, вы можете сбросить свой пароль, 
    перейдя по этой ссылке: </p> <a href="{}" style="background-color: #6C5B7B; color: #fff; padding: 10px 20px; 
    text-decoration: none; display: inline-block; margin: 20px 0;"> Нажмите здесь, чтобы сбросить пароль </a> <p 
    style="color: #355C7D; font-family: Arial, sans-serif;">Спасибо!</p> </body> </html> """.format(link)

    msg.body = 'Следуйте этой ссылке для сброса вашего пароля: {}'.format(link)

    try:
        mail.send(msg)
        print('Письмо отправлено!')
    except Exception as e:
        # Выводим все сообщения об ошибках в stdout
        print(e)

    return 'Письмо отправлено!'


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


def create_order():
    user_id = get_jwt_identity()
    data = request.form

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

    # TODO Проверить
    # Handle file upload
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            if len(file.read()) > MAX_FILE_SIZE:
                return jsonify({"msg": "File size exceeds the maximum limit of 15MB"}), 400
            try:
                file.seek(0)  # Reset file cursor to start
                order_directory = os.path.join(UPLOAD_DIRECTORY, str(new_order.id))

                if not os.path.exists(order_directory):
                    os.makedirs(order_directory)

                # Get the original filename, split by extension
                original_filename, original_ext = os.path.splitext(secure_filename(file.filename))

                # Add a timestamp to the filename
                filename = original_filename + "_" + date.now().strftime("%Y%m%d_%H%M%S") + original_ext

                # filename = secure_filename(file.filename)
                file_path = os.path.join(order_directory, filename)
                file.save(file_path)

                # Save the file_path in your database
                new_document = Document(
                    name=filename,
                    file_path=file_path,
                    order_id=new_order.id
                )
                db.session.add(new_document)
                try:
                    db.session.commit()
                except SQLAlchemyError as e:
                    return jsonify({"msg": "Database error occurred while saving document. " + str(e)}), 500

            except Exception as e:
                return jsonify({"msg": "Error occurred while saving file. " + str(e)}), 500

        else:
            return jsonify({"msg": "Invalid file type. Only .pdf, .jpg, .jpeg, .png, .gif files are allowed."}), 400

    return jsonify({"msg": "Order created successfully!"}), 201


def update_order(order_id):
    data = request.get_json()

    if not data:
        return jsonify({"msg": "No data provided"}), 400

    order = Order.query.get(order_id)

    if not order:
        return jsonify({"msg": "Order not found"}), 404

    if 'status' in data:
        order.status = data['status']

    if 'client_id' in data:
        user = User.query.get(data['client_id'])
        if not user:
            return jsonify({"msg": "User not found"}), 404
        order.client_id = user.id

    if 'service_id' in data:
        service = Service.query.get(data['service_id'])
        if not service:
            return jsonify({"msg": "Service not found"}), 404
        order.service_id = service.id

    if 'order_date' in data:
        try:
            order.order_date = date.strptime(data['order_date'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"msg": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400

    try:
        db.session.commit()
    except SQLAlchemyError as e:
        return jsonify({"msg": "Database error occurred. " + str(e)}), 500

    return jsonify({"msg": "Order updated successfully!"}), 200


def delete_order(order_id):
    data = request.get_json()
    if 'id' not in data:
        return jsonify({"msg": "Missing order_id parameter"}), 400

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"msg": "Order not found"}), 404

    db.session.delete(order)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        return jsonify({"msg": "Database error occurred. " + str(e)}), 500

    return jsonify({"msg": "Order deleted successfully!"}), 200
