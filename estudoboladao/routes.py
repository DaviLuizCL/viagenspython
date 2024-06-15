from flask import render_template, url_for, redirect, flash, request
from estudoboladao import app, database, bcrypt
from estudoboladao.forms import FormLogin, FormCriarConta
from estudoboladao.models import Usuario

lista_usuarios = ['Lira', 'João', 'Alon', 'Alessandra', 'Amanda']
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
def usuarios():
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Login feito com sucesso no email {form_login.email.data}', 'alert-success')
        return redirect(url_for('home'))

    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(username=form_criar_conta.username.data,email=form_criar_conta.email.data,senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        #adicionar sessão
        #commit na sessao
        flash(f'Conta criada com sucesso no email {form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)

