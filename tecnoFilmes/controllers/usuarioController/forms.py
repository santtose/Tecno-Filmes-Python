from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from tecnoFilmes.models.tables import User

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('ENTRAR')

class CadastroForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cpf = StringField('CPF', validators=[DataRequired()])
    celular = StringField('Celular', validators=[DataRequired()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired(), EqualTo('pass_confirm', message='As senhas devem ser iguais')])
    pass_confirm = PasswordField('Confirmar Senha', validators=[DataRequired()])
    is_ativo = BooleanField('Ativo')
    tp_usuario = RadioField('tp_usuario', choices=[('diretoria', 'Diretoria'),('comercial', 'Comercial'),('pcp', 'PCP')])
    submit = SubmitField('CADASTRAR')
        