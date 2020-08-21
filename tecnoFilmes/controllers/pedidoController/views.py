from flask import render_template, request, Blueprint, jsonify, session
from flask_login import current_user, login_required, login_url, login_user, logout_user
from tecnoFilmes.models.tables import Pedido
from tecnoFilmes import db
from tecnoFilmes.algoritmos import sugestao_pedidos as sugestao
import pandas as pd

pedido = Blueprint('pedidos', __name__)

@pedido.route('/pedidos')
def pedidos():
    pedidos = Pedido.query.filter(Pedido.maquina==400).all()
    return render_template('pedido/pedidos.html', pedidos=pedidos, title='Pedidos e Produção')

@pedido.route('/consultaPedido', methods=['POST'])
def consulta():
    consulta = '%'+request.form.get('consulta')+'%'
    pedidos = Pedido.query.filter(Pedido.material.like(consulta)).all() 

    return render_template('pedido/pedidos.html', pedidos=pedidos, title='Pedidos e Produção')

@pedido.route('/pedidoSelecionado/<int:id>')
def pedidoSelecionado(id=0):
    selecionado = Pedido.query.filter_by(id=id).first()
    melhor_solucao = sugestao.busca_melhor_solucao(selecionado)
    dfMateriais = sugestao.retornaMateriais()
    return render_template('pedido/pedidoSelecionado.html', melhor_solucao=melhor_solucao.to_dict(orient='records'), dfMateriais = dfMateriais.to_dict(orient='records'))

@pedido.route('/pedidoAgrupado/<path:material>')
def consultaPedidoAgrupado(material=""):
    # consulta = '%'+request.form.get('txtConsulta')+'%'
    # pedidos = Pedido.query.filter(Pedido.material.like(material)).all()
    print(material)
    #agrupados = sugestao.agrupa_pedidos(material)
    agrupados = sugestao.cria_agrupamentos(material)
    #session['agrupados'] = agrupados
    #session['material'] = material
    agrupados = agrupados.sort_values(by=['PACK', 'BESTSOL','REFILE'], ascending=True)
    return render_template('pedido/pedidoAgrupado.html', agrupados=agrupados.to_dict(orient='records'))

@pedido.route('/detalheAgrupamento/<path:largura_estoque>/<path:ped1>/<path:ped2>/<path:ped3>/<path:ped4>/<path:ped5>')
def detalheAgrupamento(largura_estoque="", ped1="", ped2="", ped3="", ped4="", ped5=""):

    #vamos criar a lista de pedidos para facilitar o envio das informações
    list_pedidos = []
    list_pedidos.append(int(ped1))
    list_pedidos.append(int(ped2))
    list_pedidos.append(int(ped3))
    list_pedidos.append(int(ped4))
    list_pedidos.append(int(ped5))
    print(list_pedidos)
    dfMateriais = sugestao.carregaGridMateriais(largura_estoque,list_pedidos)
    dfPedidos = sugestao.carregaGridPedidos(list_pedidos,dfMateriais)
    list_pedidos=[]
    return render_template('pedido/detalheAgrupamento.html', dfMateriais=dfMateriais.to_dict(orient='records'), dfPedidos = dfPedidos.to_dict(orient='records'))
