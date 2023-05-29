# переименовать в ruex ??
# модуль flask приложения, должен содержать app = Flask(__name__)
# добавить logger
# логгирование
from flask import Flask
from flask_mail import Mail
# в модуле tests проверка на name error локально
# невыполняющиеся импорты
# желательно проверить все IF


from config import DevelopmentConfig

app = Flask(__name__) #
app.config.from_object(DevelopmentConfig) #
mail = Mail(app)


import views
