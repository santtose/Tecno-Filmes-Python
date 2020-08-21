from flask import render_template, request, Blueprint
from flask_login import current_user, login_required, login_url, login_user, logout_user
from tecnoFilmes import db

bi = Blueprint('business', __name__)

@bi.route('/graficos')
def graficos():
    return render_template('BI/graficos.html', title='BI')
    