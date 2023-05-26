# модуль с функициями и классами для реализации бизнес логики приложения
# TODO данные почты в отдельный файл
# try catch уязвимых областей
# валидация данных
import datetime

from flask_bcrypt import Bcrypt

from models import Service  # order_service
from flask_mail import Message
from flask import request, url_for, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity
from main import mail
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import utils
from models import User, db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from main import app
import os

# create_user
# confirm_user

bcrypt = Bcrypt(app)

smtp_server = os.getenv('SMTP_SERVER')
port = 587  # For starttls
username = os.getenv('SMTP_USERNAME')
password = os.getenv('SMTP_PASSWORD')


# def register():
#     # получаем данные пользователя из запроса
#     email = request.json['email']
#     password = request.json['password']
#
#     # Создать нового пользователя в базе данных
#     user_id = create_user(email, password)
#
#     # Создать токен JWT для подтверждения регистрации
#     token = create_access_token(identity=user_id, expires_delta=False)
#
#     # Отправить письмо на почту пользователя
#     msg = Message('Подтверждение регистрации', recipients=[email])
#     msg.body = f'Для подтверждения регистрации перейдите по ссылке: {url_for("confirm_registration", token=token, _external=True)}'
#     mail.send(msg)
#
#     return {'message': 'Регистрация прошла успешно. Проверьте свою почту для подтверждения регистрации.'}, 201


# def register():
#     username = request.json.get('username', None)
#     password_hash = request.json.get('password', None)  # добавить хэш функцию
#
#     if not username or not password_hash:
#         return jsonify({'msg': 'Username or password is missing'}), 400
#
#     # проверка, существует ли пользователь
#     user = User.query.filter_by(username=username).first()
#     if user:
#         return jsonify({'msg': 'User already exists'}), 400
#
#     # email = request.json.get('email', None)
#     # Получаем первый свободный id
#     first_free_id = db.session.query(func.min(User.id + 1)). \
#         filter(~User.id.in_(db.session.query(User.id)))
#     new_user = User(id=first_free_id, username=username, password_hash=password_hash)
#
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User created successfully'}), 201


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


# TODO вынести сервер в глобальную переменную
# TODO вынести почту и пароль в глобальные переменные
def register():
    data = request.get_json()

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8') # сравнить с изначальным bcrypt из views
    expires = datetime.timedelta(days=1)  # make sure to set this to a reasonable value
    token = create_access_token(identity=data['email'], expires_delta=expires)
    # создания пользователя после успешной отправки сообщения на почту
    # сообщение на почту от небезопасного приложения
    # распознавание как спам smtp сервером
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
    except IntegrityError:  # all fields are unique
        return jsonify(message="User with that username or email already exists"), 400
    # TODO расположение токена
    msg = MIMEText('Your confirmation link is {}'.format(url_for('confirm_email', token=token, _external=True))) # external ???
    msg['Subject'] = 'Confirm Email'
    msg['From'] = username # почта сервера
    msg['To'] = data['email']

    # s = smtplib.SMTP(smtp_server, port)
    # s.starttls()  # использование шифрования
    # s.login(username, password)
    # s.send_message(msg)
    # s.quit()

    return jsonify(url_for('confirm_email', token=token, _external=True)), 201
    # return jsonify(message="Confirmation email sent. Please confirm your email."), 201


def reset_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"msg": "User not found"}), 404
    email = user.email
    expires = datetime.timedelta(hours=24)  # Token will expire in 24 hours
    token = create_access_token(identity=email, expires_delta=expires)

    msg = MIMEMultipart()
    msg['From'] = username # "your_email@example.com"
    msg['To'] = email
    msg['Subject'] = 'Password Reset Request'
    # TODO расположение токена
    link = url_for('api_reset_password_token', reset_token=token, _external=True)

    html = """
    <html>
      <body>
        <h1 style="color: #355C7D; font-family: Arial, sans-serif;">Hello!</h1>
        <p style="color: #355C7D; font-family: Arial, sans-serif;">
          We received a request to reset your password. If you didn't make the request, just ignore this email. 
          Otherwise, you can reset your password using this link:
        </p>
        <a href="{}" style="background-color: #6C5B7B; color: #fff; padding: 10px 20px; text-decoration: none; display: inline-block; margin: 20px 0;">
          Click here to reset your password
        </a>
        <p style="color: #355C7D; font-family: Arial, sans-serif;">Thank you!</p>
      </body>
    </html>
    """.format(link)
    # TODO красивый шаблон корпоративного письма с ссылками на сайт от ЮРЫ

    msg.attach(MIMEText(html, 'html'))

    msg.attach(MIMEText('Follow this link to reset your password: {}'.format(link), 'plain'))

    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls() # Secure the connection
        server.ehlo() # Can be omitted
        server.login(username, password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.close()

        print('Email sent!')
    except Exception as e:
        # Print any error messages to stdout
        print(e)

    return 'Email sent!'


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
