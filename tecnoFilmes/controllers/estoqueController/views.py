from flask import render_template, request, Blueprint, jsonify
from tecnoFilmes.models.tables import Estoque
from tecnoFilmes import db

estoque = Blueprint('estoques', __name__)

@estoque.route('/estoques')
def estoques():
    estoques = Estoque.query.all()
    return render_template('estoque/estoques.html', estoques=estoques)
