# переименовать в ruex ??
# модуль flask приложения, должен содержать app = Flask(__name__)
# добавить logger
# логгирование
from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
# в модуле tests проверка на name error локально
# невыполняющиеся импорты
# желательно проверить все IF


from config import DevelopmentConfig

app = Flask(__name__, template_folder='website_ruex', static_folder='website_ruex') #
CORS(app)
app.config.from_object(DevelopmentConfig) #
mail = Mail(app)
app.config['JSON_AS_ASCII'] = False


import views
