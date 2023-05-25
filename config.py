# модуль с настройками приложения
# перенести все настройки
import os


class DevelopmentConfig:
    DEBUG = True
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')