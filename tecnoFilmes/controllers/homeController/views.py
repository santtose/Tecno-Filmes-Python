from flask import render_template, request, Blueprint
from flask_login import current_user, login_required, login_url, login_user, logout_user
from tecnoFilmes import db

home = Blueprint('homes', __name__)

@home.route('/')
@login_required
def index():
    return render_template('home/index.html', title='Home')

@home.route('/diretoria')
def diretoria():
    return render_template('home/diretoria.html', title='Diretoria')

@home.route('/comercial')
def comercial():
    return render_template('home/comercial.html', title='Comercial')

@home.route('/pcp')
def pcp():
    return render_template('home/pcp.html', title='PCP')

