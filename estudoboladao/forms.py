from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from estudoboladao. models import Usuario


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre outro e-mail ou faça login para continuar')




class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    botao_submit_login = SubmitField('Fazer Login')


class FormCriarViagem(FlaskForm):
    destino = StringField('Destino', validators=[DataRequired(), Length(2, 50)])
    data_inicio = DateField('Data de início', format='%Y-%m-%d')
    data_termino = DateField('Data de término', format='%Y-%m-%d')
    roteiro = StringField('Roteiro da viagem', validators=[DataRequired(), Length(5, 1000)])
    botao_submit_criarViagem = SubmitField('Criar viagem')

    def validate_data_termino(self, field):
        if self.data_inicio.data and field.data:
            if field.data < self.data_inicio.data:
                raise ValidationError('A data de término deve ser posterior à data de início.')

