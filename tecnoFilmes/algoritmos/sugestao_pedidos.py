import pandas as pd
from tecnoFilmes import db
from ortools.linear_solver import pywraplp
from tecnoFilmes.models.tables import Estoque
from tecnoFilmes.models.tables import Pedido
from tecnoFilmes.models.classes import sugestaoPedido
from itertools import combinations_with_replacement, combinations
from ortools.algorithms import pywrapknapsack_solver
from sqlalchemy import func
import pandas.io.sql as psql

def busca_melhor_solucao(pedido):
    cols = ['op','largura','item', 'quantidade','metros', 'endereco','area','cod_barra','refile']
    largura = pedido.largura
    material = pedido.material
    metros = pedido.comprimento
    largura_permitida = largura+15
    retorno =[]
    list_items = []
    estoque = Estoque.query.filter_by(item =material).all()
    #estoque = estoque.query.filter(largura >= largura_permitida)
    #estoque = Estoque.query.filter_by(item=material).all()
    #sugestao = sugestaoPedido(pedido, row)
    #for row in estoque:
    #    sugestao = sugestaoPedido(pedido, row)
    #    retorno.append(sugestao)

    retorno = pd.DataFrame(columns=cols)

    for row in estoque:
        refile = ((row.largura - pedido.largura)*100)/row.largura
        list_items.append(pedido.op)
        list_items.append(row.largura)
        list_items.append(row.item)
        list_items.append(row.quantidade)
        list_items.append(row.metros)
        list_items.append(row.endereco)
        list_items.append(row.area) 
        list_items.append(row.cod_barra)
        list_items.append(round(refile,2))
        a_series = pd.Series(list_items, index = cols)
        retorno = retorno.append(a_series, ignore_index=True)
        list_items = []
    retorno = retorno[(retorno['largura'] >=largura) & (retorno['largura'] <= largura_permitida)]
    return retorno


def agrupa_pedidos(material):
    print(material)
    cols = ['largura_estoque','ped1','larg1', 'ped2','larg2', 'ped3','larg3','ped4','larg4','ped5','larg5','refile', 'saldo_restante']
    dfAgrupado = pd.DataFrame(columns=cols)
    max_sugestoes = 5
    num_sugestoes = 0
    estoque = Estoque.query.filter_by(item = material).order_by(Estoque.largura.asc()).all()
    pedidos = Pedido.query.filter_by(material = material).order_by(Pedido.largura).all()
    ###começar pelo estoque salvando do DF a largura, e lendo todos os pedidos e ver quais se encaixam.
    listped = []
    listlargura = []
    print("conseguiu ordenar")
    ##remove pedidos que não tem como serem agrupados
    ##Estoque do maior para o menor em largura
    for est in estoque:
        print("Entrou no FOR")
        #dfPedAgrupar = dfPedidos_editado.sample(n = count_pedidos)
        #Pedido ordenar do menor para o maior em largura.
        pedidos_agrupar = pedidos
        larguraEstoque = est.largura
        print("Encontrando Combinações para Lagura: {}".format(larguraEstoque))
        saldoEstoque = larguraEstoque
        listped.append(larguraEstoque)
        soma = 0
        num_sugestoes = 0
        for ped in pedidos_agrupar:
            print(ped.op)
            largura_pedido = ped.largura
            op = ped.op
            if num_sugestoes <= max_sugestoes:
                if saldoEstoque != 0 and soma != larguraEstoque:
                    if largura_pedido <= saldoEstoque:
                        num_sugestoes+=1
                        listped.append(int(op))
                        listped.append(round(largura_pedido,0))
                        saldoEstoque = saldoEstoque - largura_pedido
                        soma = soma + largura_pedido
            #else:
                #break

        #A lista precisa ter 13 itens
        if len(listped) < 13:
            while len(listped) < 13:
                listped.append(0)
        listped[11] = round(((saldoEstoque * 100)/larguraEstoque),2)
        print(saldoEstoque)
        listped[12] = saldoEstoque
        a_series = pd.Series(listped, index = dfAgrupado.columns)
        dfAgrupado = dfAgrupado.append(a_series, ignore_index=True)
        #Remove as sugestões duplicadas, devido a ter mais de um item no estoque
        dfAgrupado.drop_duplicates(keep=False, inplace=True)
        #Remove as linhas onde não foi possivel achar pedidos
        #dfAgrupado = dfAgrupado[dfAgrupado['ped1']!= 0]
        dfAgrupado = dfAgrupado.sort_values('refile',ascending=True)
        listped = []
            
    #dfAgrupado=dfAgrupado.append(listped)

    return dfAgrupado


def getOP(largura, pedidos):
    retorno = [ped for ped in pedidos if ped.largura == largura]
    print(retorno)
    return retorno

def retornaMateriais():
    pquery_consulta = "SELECT DISTINCT(MATERIAL) FROM PEDIDOS WHERE MAQUINA = 400"
    dfPedidos = psql.read_sql(pquery_consulta, db.session.bind)
    return dfPedidos

def marca_estoque(dfEstoque, largura):

    if dfEstoque[dfEstoque['largura']== largura and dfEstoque['selecionado'] == False]:
        dfEstoque[dfEstoque['largura']== largura and dfEstoque['selecionado'] == False]

    return dfEstoque

def create_data_model(list_prioridade, list_pedido, list_estoque):
    """Create the data for the example."""
    data = {}
    weights = list_pedido
    values = list_prioridade
    data['weights'] = weights
    data['values'] = values
    data['items'] = list(range(len(weights)))
    data['num_items'] = len(weights)
    num_bins = len(list_estoque)
    data['bins'] = list(range(num_bins))
    #data['bin_capacities'] = [1900,1520,870,925,1150,465]
    data['bin_capacities'] = list_estoque
    return data

def cria_agrupamentos_OLD(material):
    cols = ['cod_barra','largura_estoque','ped1','larg1', 'ped2','larg2', 'ped3','larg3','ped4','larg4','ped5','larg5','refile', 'saldo_restante']
    dfAgrupado = pd.DataFrame(columns=cols)
    dfResultado = pd.DataFrame()
    list_solucao = []
    query_consulta = "SELECT * FROM PEDIDOS WHERE MAQUINA=400"
    dfPedidos = psql.read_sql(query_consulta, db.session.bind)
    query_estoque = "select * from estoque"
    dfEstoque = psql.read_sql(query_estoque, db.session.bind)

    dfEstoque['selecionado'] = pd.Series(False, index=dfEstoque.index)
    print(dfEstoque.head())

    item_estoque = material
    dfPedidoComb = dfPedidos[dfPedidos['material']==item_estoque]
    list_op = list(dfPedidoComb['op'].astype(int))
    list_pedido = list(dfPedidoComb['largura'].astype(int))
    list_estoque = list(dfEstoque[dfEstoque['item']==item_estoque]['largura'].astype(int))
    list_estoque.sort(reverse=True)
    list_pedido.sort()
    data = create_data_model(list_op,list_pedido, list_estoque)
    # Create the mip solver with the CBC backend.
    solver = pywraplp.Solver('simple_mip_program',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    # Variables
    # x[i, j] = 1 if item i is packed in bin j.
    x = {}
    for i in data['items']:
        for j in data['bins']:
            x[(i, j)] = solver.IntVar(0, 1, 'x_%i_%i' % (i, j))

    # Constraints
    # Each item can be in at most one bin.
    #for i in data['items']:
        #solver.Add(sum(x[i, j] for j in data['bins']) <= 1)
    # The amount packed in each bin cannot exceed its capacity.
    for j in data['bins']:
        solver.Add(
            sum(x[(i, j)] * data['weights'][i]
                for i in data['items']) <= data['bin_capacities'][j])

    # Objective
    objective = solver.Objective()

    for i in data['items']:
        for j in data['bins']:
            objective.SetCoefficient(x[(i, j)], data['values'][i])
    objective.SetMaximization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        #print('Total packed value:', objective.Value())
        total_weight = 0
        for j in data['bins']:
            bin_weight = 0
            bin_value = 0
            #print('Bin ', j, '\n')
            larguraEstoque = data['bin_capacities'][j]
            list_solucao.append(str(dfEstoque[dfEstoque['largura']==larguraEstoque]['cod_barra'].values[0]))
            list_solucao.append(larguraEstoque)
            largura_soma = 0

            for i in data['items']:
                if x[i, j].solution_value() > 0:
                    #print('Item', i, '- weight:', data['weights'][i], ' value:',
                          #data['values'][i])
                    bin_weight += data['weights'][i]
                    bin_value += data['values'][i]
                    list_solucao.append(data['values'][i])
                    largura_soma = largura_soma + data['weights'][i]
                    list_solucao.append(data['weights'][i])
            refile = ((larguraEstoque - largura_soma)*100)/larguraEstoque
            if refile <= 10:
                while(len(list_solucao)<14):
                    list_solucao.append(0)  
                list_solucao[12] = round(refile,2)
                list_solucao[13] = larguraEstoque - largura_soma    
                a_series = pd.Series(list_solucao, index = dfAgrupado.columns)
                dfAgrupado = dfAgrupado.append(a_series, ignore_index=True)
            list_solucao = []
            #print('Packed bin weight:', bin_weight)
            #print('Packed bin value:', bin_value)
            #print()
            total_weight += bin_weight
        #print('Total packed weight:', total_weight)
    else:
        print('The problem does not have an optimal solution.')
    dfAgrupado.drop_duplicates(keep=False, inplace=True)
    dfAgrupado = dfAgrupado[dfAgrupado['ped1']!=0]
    dfAgrupado = dfAgrupado.sort_values('refile',ascending=True)
    return dfAgrupado

def agrupa_pedidos_combination(material):
    print(material)
    cols = ['largura_estoque','ped1','larg1', 'ped2','larg2', 'ped3','larg3','ped4','larg4','ped5','larg5','refile', 'saldo_restante']
    dfAgrupado = pd.DataFrame(columns=cols)
    max_sugestoes = 5
    num_sugestoes = 0
    estoque = Estoque.query.filter_by(item = material).order_by(Estoque.largura.asc()).all()
    largura_max = db.session.query(func.max(Estoque.largura)).scalar()
    print(largura_max)
    pedidos = Pedido.query.filter_by(material = material).order_by(Pedido.largura).all()
    print(type(pedidos))
    ###começar pelo estoque salvando do DF a largura, e lendo todos os pedidos e ver quais se encaixam.
    listped = []
    listlargura = []
    print("conseguiu ordenar")
    lista_comb = []
    for ped in pedidos:
        op_largura = [ped.op,ped.largura]
        lista_comb.append(op_largura)
            
    lista_comb = list(lista_comb)
    tupla_zero = [0,0]
    lista_comb.append(tupla_zero)
    lista_corrigida = []
    lista_refile=[]
    soma = 0
    lista_combinada = list(combinations(lista_comb, max_sugestoes))
    print("total de combinações: {}".format(len(lista_combinada)))
    for i in lista_combinada:
        soma = 0
        print(i)
        for item in i:
            soma = soma + item[1]
        if soma <= largura_max:
            lista_corrigida.append(i)
    #lista_combinada = [item for item in lista_combinada if sum(item[1]) <= largura_max]
    print("total de combinações: {}".format(len(lista_corrigida)))
    #print(lista_corrigida)
    ##remove pedidos que não tem como serem agrupados
    ##Estoque do maior para o menor em largura
    #for est in estoque:
    #    print("Entrou no FOR")
    #    larguraEstoque = est.largura
    #    num_sugestoes = 0
    #    for item in lista_corrigida:
    #        print(item)
    #        soma = 0
    #        for i in item:
    #            soma = soma + i[1]
    #        saldo = larguraEstoque - soma
    #        refile = ((larguraEstoque - soma)*100)/larguraEstoque
    #        if refile <=2:
    #            listped.append(larguraEstoque)
    #            for usar in item:
    #                #PRecisa puxar a OP.
    #                print(usar)
    #                listped.append(usar[0])
    #                listped.append(usar[1])
    #            listped.append(round(refile))
    #            listped.append(saldo)
    #            a_series = pd.Series(listped, index = dfAgrupado.columns)
    #            dfAgrupado = dfAgrupado.append(a_series, ignore_index=True)
    #            listped = []


        #Remove as sugestões duplicadas, devido a ter mais de um item no estoque
    #    dfAgrupado.drop_duplicates(keep=False, inplace=True)
        #Remove as linhas onde não foi possivel achar pedidos
        #dfAgrupado = dfAgrupado[dfAgrupado['ped1']!= 0]
    #    dfAgrupado = dfAgrupado.sort_values('refile',ascending=True)
    #    listped = []
            
    #dfAgrupado=dfAgrupado.append(listped)

    return dfAgrupado

def carregaGridMateriais(largura_estoque, list_pedidos):
    #Consulta o banco de dados para preencher os dataframes de pedido e estoque
    query_consulta = "SELECT * FROM PEDIDOS"
    dfPedidos = psql.read_sql(query_consulta, db.session.bind)
    query_estoque = "select * from estoque"
    dfEstoque = psql.read_sql(query_estoque, db.session.bind)
    #define a variavel material com base em um dos pedidos
    pedido_consulta = int(list_pedidos[0])
    material = list(dfPedidos[dfPedidos['op']== pedido_consulta]['material'].astype(str))
    #Filtra os itens de estoque com base no material
    dfEstoqueFiltrado = dfEstoque[dfEstoque['item']==material[0]]
    #filtra o estoque pela largura
    print(largura_estoque)
    dfEstoqueFiltrado = dfEstoqueFiltrado[dfEstoqueFiltrado['largura']==int(largura_estoque)]
    print(dfEstoqueFiltrado.head(10))
    #Filtra os pedidos com base no material
    dfPedidosFiltrado = dfPedidos[dfPedidos['material'] == material[0]]

    #define as colunas do que deve ser exibido na Grid de Materiais
    cols = ['cod_item', 'cod_barras', 'largura', 'metros', 'localizacao', 'item', 'saldo_metros']
    #Cria o DataFrame
    dfMateriais = pd.DataFrame(columns=cols)
    total_metros_pedido = 0
    for item in list_pedidos:
        #metros_pedido = dfPedidosFiltrado.loc[dfPedidosFiltrado['op']==item,'comprimento'].item()
        if item > 0:
            metros_pedido = list(dfPedidosFiltrado[dfPedidosFiltrado['op']==int(item)]['comprimento'].astype(int))
            total_metros_pedido = total_metros_pedido + metros_pedido[0]
            print(total_metros_pedido)
        metros_pedido=[]

    list_materiais = []
    print(dfEstoqueFiltrado.info())
    saldo_estoque = 0
    for Index, item in dfEstoqueFiltrado.iterrows():
        list_materiais.append(item['codigo_item'])
        list_materiais.append(item['cod_barra'])
        list_materiais.append(item['largura'])
        list_materiais.append(item['metros'])
        list_materiais.append(item['endereco'])
        list_materiais.append(item['item'])
        if total_metros_pedido > 0:
            total_metros_pedido = total_metros_pedido - int(item['metros'])
            list_materiais.append(total_metros_pedido)
        else:
            list_materiais.append(0)
            break
        a_series = pd.Series(list_materiais, index = dfMateriais.columns)
        dfMateriais = dfMateriais.append(a_series, ignore_index=True)
        list_materiais = []

    print(dfMateriais.info())
    return dfMateriais

def carregaGridPedidos(list_pedidos, dfEstoque):
    #Consulta o banco de dados para preencher os dataframes de pedido e estoque
    query_consulta = "SELECT * FROM PEDIDOS"
    dfPedidos = psql.read_sql(query_consulta, db.session.bind)
    dfPedidos_filtrado = pd.DataFrame(columns=dfPedidos.columns)
    for item in list_pedidos:
        dfPedidos_filtrado = dfPedidos_filtrado.append(dfPedidos[dfPedidos['op']==item],ignore_index=True)
    
    print(dfPedidos_filtrado.info())
    return dfPedidos_filtrado




## Novas Implementações

def mochila(list_pedidos, list_larguras, capacidade):
    #Cria o DataFrame para retorno das informações
    dfRetorno = pd.DataFrame()
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    values = list_pedidos
    #print("Mochila lista de OPS: {}".format(values))
    weights = list_larguras
    #print("Mochila Lista de Larguras: {}".format(weights))
    capacities = capacidade

    solver.Init(values, weights, capacities)
    computed_value = solver.Solve()

    packed_items = []
    packed_weights = []
    packed_op = []
    total_weight = 0
    #print('Total value =', computed_value)
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            packed_op.append(values[i])
            packed_items.append(i)
            packed_weights.append(weights[0][i])
            total_weight += weights[0][i]
    #print('Total weight:', total_weight)
    #print('Packed items:', packed_items)
    #print('Packed_weights:', packed_weights)
    if len(packed_op) > 0:
        dfRetorno['OP'] = packed_op
        dfRetorno['Largura'] = packed_weights
        return dfRetorno
    else:
        return None


def calculaRefile(dfRetorno, largura_estoque):
    list_larguras = dfRetorno['Largura'].astype(int)
    total_largura = sum(list_larguras)
    diferenca = largura_estoque - total_largura
    refile = (diferenca*100)/largura_estoque
    return refile


def gera_melhor_solucao(dfPedidos_filtrado, dfEstoque_filtrado):
    lista_pack = []
    pack = {}
    idPack = 0
    for Index_pedido, pedido in dfPedidos_filtrado.iterrows():
        #dfEstoque_temp = dfEstoque_filtrado[dfEstoque_filtrado['largura']>=pedido['largura']]
        #print("OP {}".format(pedido['op']))
        for Index_estoque, material in dfEstoque_filtrado.iterrows():
            #print("Estoque Largura: {}".format(material['largura']))
            largura_estoque = material['largura']
            largura_estoque = int(largura_estoque)
            largura_pedido = pedido['largura']
            #print("Pedido Largura: {}".format(largura_pedido))
            diferenca = largura_estoque - largura_pedido
            refile = (diferenca * 100)/largura_estoque
            #print("REFILE: {}".format(refile))
            if refile > 0 and refile <= 5:
                saldo = material['metros'] - pedido['comprimento']
                if saldo >= 0:
                    #pack['SALDO'] = abs(saldo)
                    idPack = idPack + 1
                    pack['OP'] = pedido['op']
                    pack['IDPEDIDO'] = Index_pedido
                    pack['PACK'] = idPack
                    pack['LARGURA'] = pedido['largura']
                    pack['COMPRIMENTO'] = pedido['comprimento']
                    pack['LARGESTOQUE'] = material['largura']
                    pack['METROSESTOQUE'] = material['metros']
                    pack['CODBARRA'] = material['cod_barra']
                    pack['IDESTOQUE'] = Index_estoque
                    pack['REFILE'] = round(refile,2)
                    pack['BESTSOL'] = True
                    pack['SALDO'] = 0
                    lista_pack.append(pack)
                    pack = {}
                break;
            #else:
                #break;
            pack = {}
                
    if len(lista_pack) > 0:
        dfFinal = pd.DataFrame.from_dict(lista_pack) 
        #print(dfFinal.info())
        return dfFinal
    else:
        return None
                

def cria_agrupamentos(material):

    query_consulta = "SELECT * FROM PEDIDOS"
    dfPedidos = psql.read_sql(query_consulta, db.session.bind)
    query_estoque = "select * from estoque"
    dfEstoque = psql.read_sql(query_estoque, db.session.bind)
    dfPedidos_filtrado = dfPedidos[dfPedidos['material']==material]
    dfEstoque_filtrado = dfEstoque[dfEstoque['item']==material]
    dfEstoque_filtrado.set_index('id', inplace=True)
    dfPedidos_filtrado.set_index('id',inplace = True)
    ##Busca encontrar a melhor solução, e ja gera o dataframe do Pack
    dfPackFull = gera_melhor_solucao(dfPedidos_filtrado,dfEstoque_filtrado)
    print(dfPackFull.head(100))
    #Antes de continuar precisamos remover os pedidos que possuem uma BESTSOL
    for Index, bestsol in dfPackFull.iterrows():
        print("DELETA OP: {}".format(bestsol['OP']))

        #index = dfPedidos_filtrado[dfPedidos_filtrado['op']==bestsol['OP']].index.values[0]
        index = bestsol['IDPEDIDO']
        print("DELETA INDEX: {}".format(index))
        dfPedidos_filtrado.drop(index, inplace=True)
        print("DELETOU PEDIDO")
        #Remove também do estoque
        #index_estoque = dfEstoque_filtrado[dfEstoque_filtrado['cod_barra']==bestsol['IDESTOQUE']].index.values[0]
        index_estoque = bestsol['IDESTOQUE']
        print("COD BARRA DELETAR: {}".format(index_estoque))
        dfEstoque_filtrado.drop(index_estoque, inplace=True)

    ##dfPackTratar = dfPackFull.loc[dfPackFull['BESTSOL']==False,'OP']
    #list_pedidos = list(dfPedidos_filtrado.loc[dfPackFull['BESTSOL']==False,'OP'])
    #list_larguras = [list(dfPackFull.loc[dfPackFull['BESTSOL']==False,'LARGURA'].astype(int))]
    list_pedidos = list(dfPedidos_filtrado['op'].astype(int))
    list_larguras = [list(dfPedidos_filtrado['largura'].astype(int))]
    cols_pack_principal = ['PACK','OP', 'LARGURA', 'COMPRIMENTO', 'LARGESTOQUE','REFILE', 'METROSESTOQUE', 'SALDO','IDESTOQUE','BESTSOL']
    dfPack = pd.DataFrame(columns=cols_pack_principal)
    lista_pack = []
    #Esse deve ser o dicionario com os pedidos do PACK para adicionar no banco de dados.
    pack = {}
    idPack = 0
    print(dfPackFull[dfPackFull['PACK']==dfPackFull['PACK'].max()]['PACK'].values[0])
    idPack = dfPackFull[dfPackFull['PACK']==dfPackFull['PACK'].max()]['PACK'].values[0]
    print(idPack)
    #while(len(list_pedido) > 0):

    for Index_estoque, material in dfEstoque_filtrado.iterrows():
        #print(Index)
        largura_estoque = material['largura']
        largura_estoque = int(largura_estoque)
        deleta_estoque = False
        #print("inicio na ,largura de estoque {}".format(largura_estoque))
        largura_estoque_list = []
        largura_estoque_list.append(largura_estoque)
        dfRetorno = mochila(list_pedidos,list_larguras, largura_estoque_list)
        if dfRetorno is not None:
            #print(dfRetorno.head(1))
            refile = calculaRefile(dfRetorno,largura_estoque)
            # Valida se o Refile esta dentro do esperado
            if refile <=6:            
                #valida cada um dos pedidos se ultrapassa a metragem
                idPack = idPack + 1
                for Index_retorno, item in dfRetorno.iterrows():
                    ordem_producao = item['OP']
                    comprimento_OP = dfPedidos_filtrado.loc[dfPedidos_filtrado['op']==ordem_producao,'comprimento'].values[0]
                    metros_estoque = material['metros']
                    saldo = metros_estoque - comprimento_OP
                    pack['PACK'] = idPack
                    #dfPackFull.at[dfPackFull[dfPackFull['OP']==ordem_producao].index.values[0],'PACK'] = idPack
                    pack['OP'] = item['OP']
                    pack['LARGURA'] = dfPedidos_filtrado.loc[dfPedidos_filtrado['op']==item['OP'],'largura'].values[0]
                    pack['COMPRIMENTO'] = dfPedidos_filtrado.loc[dfPedidos_filtrado['op']==item['OP'],'comprimento'].values[0]
                    pack['IDPEDIDO'] = dfPedidos_filtrado[dfPedidos_filtrado['op']==item['OP']].index.values[0]
                    pack['LARGESTOQUE'] = material['largura']
                    pack['METROSESTOQUE'] = material['metros']
                    pack['CODBARRA'] = material['cod_barra']
                    pack['IDESTOQUE'] = Index_estoque
                    pack['REFILE'] = round(refile,2)
                    pack['BESTSOL'] = False
                    #se o saldo é menor que zero então precisamos procurar outro item de estoque para finalizar o pedido
                    if saldo < 0:
                        #print("encontrou saldo para o pedido: {} de {}".format(item['OP'],abs(saldo)))
                        pack['SALDO'] = abs(saldo)
                        #procurar um item de estoque com a mesma largura que não seja o utilizado nesse PACK.
                        dfEstoque_adicional = dfEstoque_filtrado.loc[dfEstoque_filtrado['metros'] >= abs(saldo)]
                        #vamos filtrar o item de estoque que tenha a mesma largura ou maior
                        dfEstoque_adicional = dfEstoque_adicional[dfEstoque_adicional['largura'].between(item['Largura'], item['Largura']+15, inclusive=True)]
                        #Devemos excluir o item de estoque que estamos usando no momento
                        dfEstoque_adicional = dfEstoque_adicional.loc[dfEstoque_adicional.index != Index]
                        #print(dfEstoque_adicional.head(5))
                    else:
                        pack['SALDO'] = 0                    
                    lista_pack.append(pack)
                    pack = {}
                #Remove também do estoque
                #index_estoque = dfEstoque_filtrado[dfEstoque_filtrado['cod_barra']==material['cod_barra']].index.values[0]
                dfEstoque_filtrado.drop(Index_estoque, inplace=True)
    dfFinal = pd.DataFrame.from_dict(lista_pack)
    dfPackFull = dfPackFull.append(dfFinal, ignore_index=True)
    return dfPackFull