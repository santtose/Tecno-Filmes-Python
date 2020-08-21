import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykey'

#####################
# Conexão com o Banco
#####################
#'sqlite:///' + os.path.join(basedir, 'data.sqlite')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://homtecnofilmes:Xbits@123@homtecnofilmes.postgresql.dbaas.com.br:5432/homtecnofilmes'
#'postgres://tzymnmwpdmjtmz:7c4d80c87e6884cb827bad9575f8efee3563e54d49db6f455748d5d953be3b46@ec2-34-200-15-192.compute-1.amazonaws.com:5432/div03fv9fbmve'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

#######################
# Configuração do Login
#######################
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'

from tecnoFilmes.controllers.homeController.views import home
from tecnoFilmes.controllers.usuarioController.views import users
from tecnoFilmes.controllers.pedidoController.views import pedido
from tecnoFilmes.controllers.estoqueController.views import estoque
from tecnoFilmes.controllers.plannerController.views import planner
from tecnoFilmes.controllers.linhaDeProducaoController.views import linhaProd
from tecnoFilmes.controllers.biController.views import bi
from tecnoFilmes.errorPages.handlers import error_pages

app.register_blueprint(home)
app.register_blueprint(users)
app.register_blueprint(pedido)
app.register_blueprint(estoque)
app.register_blueprint(planner)
app.register_blueprint(linhaProd)
app.register_blueprint(bi)
app.register_blueprint(error_pages)


