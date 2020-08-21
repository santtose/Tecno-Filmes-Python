from tecnoFilmes.algoritmos.query import cargaAtividadesSql, sugestaoComPedidosSql
from tecnoFilmes.algoritmos.connection import connection
import datetime
import time
import pandas as pd

cursor = connection.cursor()

def esta_na_hora(hora, minuto, data_atual):
    if data_atual.hour == hora and data_atual.minute == minuto:
        return True
    return False

print('***** Job Carga *****')
hora_string = "09:34"

hora = int(hora_string.split(':')[0])
minuto = int(hora_string.split(':')[1])

agora = datetime.datetime.now()

if esta_na_hora(hora, minuto, agora):
    print("Realizando Insert")
    cursor.execute(cargaAtividadesSql, (agora,))
    connection.commit()

    cursor.execute(sugestaoComPedidosSql)
    sugestaoComPedidos = cursor.fetchall() 
    
    df = pd.DataFrame(sugestaoComPedidos, columns=["codigo", "nome", "id", "data"])

    # Mediana das datas agrupadas por codigo
    resultadoMediana = df.groupby('codigo')['data'].apply(lambda x: x.diff().median()).reset_index().rename(columns={"data":"mediana_dia"})
    resultadoMediana = resultadoMediana.dropna(subset=['mediana_dia'])
    
    if resultadoMediana.empty == False:
        join = pd.merge(df, resultadoMediana, on='codigo')

        # Pega a última informação da lista, ultima data
        ultimaCompra = join.groupby('codigo').tail(1)
        ultimaCompra['diferenca_datas'] = datetime.datetime.now() - ultimaCompra['data']
        #print(ultimaCompra)

        # Tempo entre últimmo pedido até data atual MAIOR que a mediana - Atividade pro dia
        atividadeDiaDf = ultimaCompra.loc[ultimaCompra.mediana_dia < ultimaCompra.diferenca_datas]
        atv = atividadeDiaDf.loc[:,['codigo','data']]
        listaAtividadeDia = atv.values.tolist()

        for i in listaAtividadeDia:
            salvar = Atividade(cliente_id=i[0],data=date.today(), usuario_id=None)
            db.session.add(salvar)
            db.session.commit() 

        # Tempo entre último pedido até a data atual MENOR que a mediana, calcula quantos dias faltam
        # para que o tempo seja o mesmo que a mediana e cria atividade para 5 dias antes - 
        # Atividade próximo 5 dias
        atividadeProximoDiaDf = ultimaCompra.loc[ultimaCompra.mediana_dia > ultimaCompra.diferenca_datas]
        # Quantos dias faltam para ser igual a mediana
        atividadeProximoDiaDf.loc[:, 'faltantes'] = atividadeProximoDiaDf.mediana_dia - atividadeProximoDiaDf.diferenca_datas
        # Subtrai 5 dias para criar atividade 5 dias antes do seu vencimento medio
        atividadeProximoDiaDf.loc[:, 'dias_atv'] = atividadeProximoDiaDf.faltantes - datetime.timedelta(days=5)
        # Traz dias positivos
        criaAtividade = atividadeProximoDiaDf.loc[atividadeProximoDiaDf.dias_atv > datetime.timedelta(days=1)]
        # criada a atividade
        criaAtividade.loc[:, 'data'] = criaAtividade.data + criaAtividade.dias_atv
        # print('***********')
        # print(criaAtividade.loc[:, 'data':'dias_atv'])
        atvProx = criaAtividade.loc[:,['codigo','data']]
        listaAtividadeProxDia = atvProx.values.tolist()

        for j in listaAtividadeProxDia:
            salvarProx = Atividade(cliente_id=j[0],data=j[1], usuario_id=None)
            db.session.add(salvarProx)
            db.session.commit()
        
        # Resto. Datas que são menores que 1 dia para serem iguais as medianas, cria atividade pro dia
        atvResto = atividadeProximoDiaDf.loc[:,['codigo','data']]
        listaAtividadeResto = atvResto.values.tolist()

        for k in listaAtividadeResto:
            salvarResto = Atividade(cliente_id=k[0],data=date.today(), usuario_id=None)
            db.session.add(salvarResto)
            db.session.commit()
