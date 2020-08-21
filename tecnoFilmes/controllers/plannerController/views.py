from flask import render_template, request, Blueprint
from flask_login import current_user, login_required, login_url, login_user, logout_user
from flask_paginate import Pagination, get_page_args, get_page_parameter
from datetime import date, datetime
from tecnoFilmes.models.tables import Cliente
from tecnoFilmes.models.tables import Pedido
from tecnoFilmes.models.tables import Atividade
from tecnoFilmes.models.tables import User
from tecnoFilmes.algoritmos.query import *
from tecnoFilmes.algoritmos.connection import connection
from tecnoFilmes import db
import time, datetime
from datetime import date
import pandas as pd
import numpy as np

planner = Blueprint('planners', __name__)

cursor = connection.cursor()

@planner.route('/planners')
def planners():

    cursor.execute(sugestaoCincoDiasSql)
    sugestaoCinco = cursor.fetchall()
    
    cursor.execute(sugestaoSql)
    clientesSugestao = cursor.fetchall()

    cursor.execute(emAtendimentoCincoSql, (current_user.id,))
    clienteEmAtendimentoCinco = cursor.fetchall()

    cursor.execute(emAtendimentoSql, (current_user.id,))
    clienteEmAtendimento = cursor.fetchall()

    if sugestaoCinco != None:
        cont = len(clientesSugestao + sugestaoCinco)
    else:
        cont = len(clientesSugestao)

    if clienteEmAtendimentoCinco != None:
        contA = len(clienteEmAtendimento + clienteEmAtendimentoCinco)
    else:
        contA = len(clienteEmAtendimento)

    return render_template('planner/planners.html', 
                            clientes=clientesSugestao, 
                            clientesAt=clienteEmAtendimento,
                            clientesCincoDias=sugestaoCinco,
                            clientesAtCincoDias=clienteEmAtendimentoCinco,
                            cont=cont, 
                            contA=contA,
                            title='Minhas Atividades')

@planner.route('/detalhes/<int:id>')
def detalhes(id=0):
    cliente = Cliente.query.filter_by(id=id).first()

    # cursor.execute(ultimosPedidosSql, (id,))
    # ultimosPedidos = cursor.fetchall()

    ultimosPedidos = Pedido.query.join(Cliente, Pedido.cliente_id == Cliente.codigo) \
                        .filter(Cliente.id == id) \
                        .order_by(Pedido.data.desc()) \
                        .limit(5).all()
            
    selectMateriais = Pedido.query.join(Cliente, Pedido.cliente_id == Cliente.codigo) \
                        .filter(Cliente.id == id) \
                        .order_by(Pedido.data.desc()) \
                        .all()

    return render_template('planner/detalhes.html', cliente=cliente,
                                                    ultimosPedidos=ultimosPedidos,
                                                    selectMateriais=selectMateriais,
                                                    title='Detalhes Cliente')

@planner.route('/acao/<int:codigo>')
def acao(codigo=0):
    atividade = Atividade.query.filter_by(cliente_id=codigo).first()