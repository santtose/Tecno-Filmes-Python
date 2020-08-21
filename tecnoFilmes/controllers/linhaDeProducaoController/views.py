from flask import render_template, request, Blueprint
from tecnoFilmes import db

linhaProd = Blueprint('linhasProd', __name__)

@linhaProd.route('/producao')
def producao():
    return render_template('linhaProducao/producao.html')
