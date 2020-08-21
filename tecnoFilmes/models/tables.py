from tecnoFilmes import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True)
    cpf = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(64), index=True)
    celular = db.Column(db.String(20))
    telefone = db.Column(db.String(20))
    login = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_ativo = db.Column(db.Boolean, default=False)
    tp_usuario = db.Column(db.String(20))
    atividade = db.relationship('Atividade', backref='ativi_cli')

    def __init__(self, email, login, password, nome, cpf, celular, telefone, is_ativo, tp_usuario):
        self.email = email
        self.login = login
        self.nome = nome
        self.cpf = cpf
        self.celular = celular
        self.telefone = telefone
        self.is_ativo = is_ativo
        self.tp_usuario = tp_usuario
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    def __repr__(self):
        return f'Login {self.login}'


class Cliente(db.Model):

    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.Integer, unique=True)
    nome = db.Column(db.String(75))
    nome_fantasia = db.Column(db.String(75))
    cnpj_cpf = db.Column(db.String(20), unique=True, index=True)
    tipo_cliente = db.Column(db.Integer)
    fone = db.Column(db.String(11))
    e_mail = db.Column(db.String(75))
    segmento_mercado = db.Column(db.Integer)
    segmento_descricao = db.Column(db.String(75))
    subsegmento_mercado = db.Column(db.Integer)
    subsegmento_descricao = db.Column(db.String(75))
    porte = db.Column(db.String(75))
    tipo_vinculo = db.Column(db.String(75))
    pedido = db.relationship('Pedido', backref='ordem_prod')
    atividade = db.relationship('Atividade', backref='atividade_cli')

    def __init__(self, codigo, nome, nome_fantasia, cnpj_cpf, tipo_cliente, fone, e_mail
                     ,segmento_mercado, segmento_descricao, subsegmento_mercado, subsegmento_descricao
                     ,porte, tipo_vinculo):
        self.codigo = codigo
        self.nome = nome
        self.nome_fantasia = nome_fantasia
        self.cnpj_cpf = cnpj_cpf
        self.tipo_cliente = tipo_cliente
        self.fone = fone
        self.e_mail = e_mail
        self.segmento_mercado = segmento_mercado
        self.segmento_descricao = segmento_descricao
        self.subsegmento_mercado = subsegmento_mercado
        self.subsegmento_descricao = subsegmento_descricao
        self.porte = porte
        self.tipo_vinculo = tipo_vinculo

    def __repr__(self):
        return f'Codigo {self.codigo}'

class Pedido(db.Model):

    __tablename__ = 'pedidos'

    id = db.Column(db.Integer, primary_key=True)
    op = db.Column(db.Integer)
    maquina = db.Column(db.Integer)
    data = db.Column(db.DateTime)
    item = db.Column(db.Integer)
    largura = db.Column(db.Float)
    d_int = db.Column(db.Integer)
    material = db.Column(db.String(65))
    quantidade = db.Column(db.Integer)
    gramatura = db.Column(db.Float)
    comprimento = db.Column(db.Float)
    saldo = db.Column(db.Integer)
    observacao = db.Column(db.String(200))
    data_embarque = db.Column(db.DateTime)
    situacao = db.Column(db.String(100))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.codigo'))

    def __init__(self, op, maquina, data, item, largura, d_int, material, quantidade, gramatura,
                        comprimento, saldo, observacao, data_embarque, situacao, cliente_id):
        self.op = op
        self.maquina = maquina
        self.cliente = cliente
        self.data = data
        self.item = item
        self.largura = largura
        self.d_init = d_init
        self.material = material
        self.quantidade = quantidade
        self.gramatura = gramatura
        self.comprimento = comprimento
        self.saldo = saldo
        self.observacao = observacao
        self.data_embarque = data_embarque
        self.situacao = situacao
        self.cliente_id = cliente_id

    def __repr__(self):
        return f'Op {self.op}'


class Estoque(db.Model):

    __tablename__ = 'estoque'

    id = db.Column(db.Integer, primary_key=True)
    codigo_item = db.Column(db.Integer)
    versao = db.Column(db.String(75))
    largura = db.Column(db.Float)
    item = db.Column(db.String(75))
    data = db.Column(db.DateTime)
    quantidade = db.Column(db.Float)
    metros = db.Column(db.Float)
    endereco = db.Column(db.String(75))
    area = db.Column(db.String(75))
    cod_barra = db.Column(db.String(100))

    def __init__(self, codigo_item, versao, largura, item, data,
                        quantidade, metros, endereco, area, cod_barra):
        self.codigo_item = codigo_item
        self.versao = versao
        self.largura = largura
        self.item = item
        self.data = data
        self.quantidade = quantidade
        self.metros = metros
        self.endereco = endereco
        self.area = area
        self.cod_barra = cod_barra

    def __repr__(self):
        return f'Codigo {self.codigo_item}'


class Maquina(db.Model):
    
    __tablename__ = 'maquina'

    id = db.Column(db.Integer, primary_key=True)
    cod_maquina = db.Column(db.Integer)
    maquina = db.Column(db.String(75))
    pistas = db.Column(db.Integer)
    largura_minima = db.Column(db.Integer)
    largura_maxima = db.Column(db.Integer)
    polegadas = db.Column(db.Integer)
    transparente = db.Column(db.Boolean)
    metalizado = db.Column(db.Boolean)
    ativo = db.Column(db.Boolean)

    def __init__(self, cod_maquina, maquina, pistas, largura_minima, largura_maxima,
                        polegadas, transparente, metalizado, ativo):
        self.cod_maquina = cod_maquina
        self.maquina = maquina
        self.pistas = pistas
        self.largura_minima = largura_minima
        self.polegadas = polegadas
        self.transparente = transparente
        self.metalizado = metalizado
        self.ativo = ativo

    def __repr__(self):
        return f'Codigo {self.cod_maquina}'


class Material(db.Model):
    
    __tablename__ = 'material'

    id = db.Column(db.Integer, primary_key=True)
    cod_material = db.Column(db.Integer)
    material = db.Column(db.String(75))
    ativo = db.Column(db.Boolean)

    def __init__(self, cod_material, material, ativo):
        self.cod_material = cod_material
        self.versao = versao
        self.largura = largura
        self.item = item
        self.data = data
        self.quantidade = quantidade
        self.metros = metros
        self.endereco = endereco
        self.area = area
        self.cod_barra = cod_barra

    def __repr__(self):
        return f'Codigo {self.cod_material}'

class Atividade(db.Model):

    __tablename__ = 'atividade'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime)
    is_finalizada = db.Column(db.Boolean, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.codigo'))

    def __init__(self, data, usuario_id, cliente_id):
        self.data = data
        self.usuario_id = usuario_id
        self.cliente_id = cliente_id

    def __repr__(self):
        return f'Data {self.data}'       

class AtividadeHistorico(db.Model):

    __tablename__ = 'atividadehistorico'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(500))
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividade.id'))
    acao_id = db.Column(db.Integer, db.ForeignKey('acao.id'))
    subacao_id = db.Column(db.Integer, db.ForeignKey('subacao.id'))
    motivoacao_id = db.Column(db.Integer, db.ForeignKey('motivoacao.id'))

    def __init__(self, descricao, atividade_id, acao_id, subacao_id):
        self.descricao = descricao
        self.atividade_id = atividade_id
        self.acao_id = acao_id
        self.subacao_id = subacao_id

    def __repr__(self):
        return f'Descricao {self.descricao}'

class Acao(db.Model):

    __tablename__ = 'acao'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50))
    is_ativa = db.Column(db.Boolean, default=False)
    atividade_historico = db.relationship('AtividadeHistorico', backref='atividade_hist')
    subacao = db.relationship('SubAcao', backref='acao')

    def __init__(self, descricao, is_ativa):
        self.descricao = descricao
        self.is_ativa = is_ativa
    
    def __repr__(self):
        return f'Descricao {self.descricao}'

class SubAcao(db.Model):
    
    __tablename__ = 'subacao'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50))
    is_ativa = db.Column(db.Boolean, default=False)
    atividade_historico = db.relationship('AtividadeHistorico', backref='ativ_hist')
    acao_id = db.Column(db.Integer, db.ForeignKey('acao.id'))

    def __init__(self, descricao, is_ativa, acao_id):
        self.descricao = descricao
        self.is_ativa = is_ativa
        self.acao_id = acao_id
    
    def __repr__(self):
        return f'Descricao {self.descricao}'

class motivoAcao(db.Model):
    
    __tablename__ = 'motivoacao'

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(50))
    is_ativa = db.Column(db.Boolean, default=False)
    atividade_historico = db.relationship('AtividadeHistorico', backref='ativ_historico')

    def __init__(self, descricao, is_ativa):
        self.descricao = descricao
        self.is_ativa = is_ativa
    
    def __repr__(self):
        return f'Descricao {self.descricao}'
