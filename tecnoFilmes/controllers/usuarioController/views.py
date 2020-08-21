from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import current_user, login_required, login_url, login_user, logout_user
from tecnoFilmes import db
from tecnoFilmes.models.tables import User
from tecnoFilmes.controllers.usuarioController.forms import CadastroForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from validate_docbr import CPF

users = Blueprint('users', __name__)

@users.route('/usuario')
@login_required
def usuario():
    usuarios = User.query.all()
    return render_template('usuario/usuario.html', usuarios=usuarios, title='Usuários')

@users.route('/consulta', methods=['POST'])
def consulta():
    consulta = '%'+request.form.get('consulta')+'%'

    usuarios = User.query.filter(User.nome.like(consulta)).all()

    return render_template('usuario/usuario.html', usuarios=usuarios, title='Usuários')

# Cadastro
@users.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    form = CadastroForm()

    if form.validate_on_submit():
        user = User(nome=form.nome.data,
                    email=form.email.data,
                    cpf=form.cpf.data,
                    celular=form.celular.data,
                    telefone=form.telefone.data,
                    login=form.login.data,
                    is_ativo=form.is_ativo.data,
                    tp_usuario=form.tp_usuario.data,
                    password=form.password.data)

        if User.find_by_email(user.email) and User.find_by_login(user.login):
            flash('E-mail já cadastrado no sistema.')
            flash('Login já cadastrado. Tente um novo.')
            return redirect(url_for('users.cadastrar'))
        elif  User.find_by_email(user.email):
            flash('E-mail já cadastrado no sistema.')
            return redirect(url_for('users.cadastrar'))
        elif User.find_by_login(user.login):
            flash('Login já cadastrado. Tente um novo.')
            return redirect(url_for('users.cadastrar'))

        validarCPF = CPF()
        if validarCPF.validate(user.cpf):      
            db.session.add(user)
            db.session.commit()
        else:
            flash('Cpf inválido. Tente novamente!')
        
        if current_user.is_authenticated and validarCPF.validate(user.cpf):
            return redirect(url_for('users.usuario'))
        elif current_user.is_authenticated and validarCPF.validate(user.cpf) == False:
            return redirect(url_for('users.cadastrar'))
        else:
            return redirect(url_for('users.login'))

    return render_template('usuario/cadastrar.html', form=form, title='Cadastrar Usuário')

# Login
@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(login=form.login.data).first()

        if user.check_password(form.password.data) and user is not None:

            login_user(user)
            #flash('Login realizado com sucesso!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('homes.index')

            return redirect(next)            
        else:
            flash('Login ou Senha inválidos')

    return render_template('usuario/login.html', form=form, title='Log-in')

# Logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/editar/<int:id>')
def editar(id=0):
    usuario = User.query.filter_by(id=id).first()
    return render_template('usuario/editar.html', usuario=usuario, title='Editar Usuário')

@users.route('/salvar_edicao', methods=['POST'])
def salvar_edicao():
    Id = int(request.form.get('id'))
    Login = request.form.get('login')
    Nome = request.form.get('nome')
    Email = request.form.get('email')
    Cpf = request.form.get('cpf')
    Celular = request.form.get('celular')
    Telefone = request.form.get('telefone')
    Password = request.form.get('password')
    Tp_usuario = request.form.get('tp_usuario')
    Is_ativo = request.form.get('is_ativo')
    Pass_confirm = request.form.get('pass_confirm')

    usuario = User.query.filter_by(id=Id).first()

    usuario.login = Login
    usuario.nome = Nome
    usuario.email = Email
    usuario.cpf = Cpf
    usuario.celular = Celular
    usuario.telefone = Telefone
    usuario.password = Password
    usuario.tp_usuario = Tp_usuario
    usuario.is_ativo = Is_ativo
    usuario.pass_confirm = Pass_confirm

    validarCPFEdit = CPF()

    if validarCPFEdit.validate(usuario.cpf): 
        db.session.commit()
    else:
        flash('Cpf inválido. Tente novamente!')

    if validarCPFEdit.validate(usuario.cpf) == False:
        return redirect(url_for('users.editar',id=usuario.id))

    return redirect(url_for('users.usuario'))

@users.route('/deletar/<int:id>')
def deletar(id=0):
    usuario = User.query.filter_by(id=id).first()
    return render_template('usuario/deletar.html', usuario=usuario, title='Excluir Usuário')

@users.route('/salvar_delecao', methods=['POST'])
def salvar_delecao():
    Id = int(request.form.get('id'))

    usuario = User.query.filter_by(id=Id).first()

    db.session.delete(usuario)
    db.session.commit()

    return redirect(url_for('users.usuario'))
