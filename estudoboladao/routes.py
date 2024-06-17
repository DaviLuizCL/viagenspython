from flask import render_template, url_for, redirect, flash, request
from estudoboladao import app, database, bcrypt
from estudoboladao.forms import FormLogin, FormCriarConta, FormCriarViagem, FormEditarViagem, FormEditarViagem
from estudoboladao.models import Usuario, Viagem
from flask_login import login_user, logout_user, current_user, login_required
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contato')
def contato():
    return render_template('contato.html')


@app.route('/viagens')
@login_required
def usuarios():
    viagens = Viagem.query.filter_by(autor=current_user).all()
    return render_template('viagens.html', viagens=viagens)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no email {form_login.email.data}', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash(f'Email ou senha incorretos, tente novamente', 'alert-danger')

    if form_criar_conta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criar_conta.senha.data)
        usuario = Usuario(username=form_criar_conta.username.data,email=form_criar_conta.email.data,senha=senha_cript)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta criada com sucesso no email {form_criar_conta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/viagem/criar', methods=['GET', 'POST'])
@login_required
def criar_viagem():
    form_criarViagem = FormCriarViagem()
    if form_criarViagem.validate_on_submit() and 'botao_submit_criarViagem' in request.form:
        viagem = Viagem(destino=form_criarViagem.destino.data,
         data_inicio=form_criarViagem.data_inicio.data,
          data_termino=form_criarViagem.data_termino.data,
           roteiro=form_criarViagem.roteiro.data,
           autor=current_user)
        database.session.add(viagem)
        database.session.commit()
        flash(f'Viagem para {form_criarViagem.destino.data}, criada com sucesso!', 'alert-success')
        return redirect(url_for('usuarios'))
    return render_template('criarviagem.html', form_criarViagem=form_criarViagem)



@app.route('/viagem/<viagem_id>', methods=['GET', 'POST'])
@login_required
def editar_viagem(viagem_id):
    viagem = Viagem.query.get(viagem_id)
    form = FormEditarViagem()
    if request.method == 'GET':
        form.destino.data = viagem.destino
        form.data_inicio.data = viagem.data_inicio
        form.data_termino.data = viagem.data_termino
        form.roteiro.data = viagem.roteiro
    elif form.validate_on_submit():
        viagem.destino = form.destino.data
        viagem.data_inicio = form.data_inicio.data
        viagem.data_termino = form.data_termino.data
        viagem.roteiro = form.roteiro.data
        database.session.commit()

    if form.validate_on_submit() and 'botao_submit_editarViagem' in request.form:
        viagem = Viagem(destino=form.destino.data,
         data_inicio=form.data_inicio.data,
          data_termino=form.data_termino.data,
           roteiro=form.roteiro.data,
           autor=current_user)
        flash(f'Viagem para {form.destino.data}, modificada com sucesso!', 'alert-success')
        return redirect(url_for('usuarios'))
    return render_template('editarviagem.html', form=form, viagem=viagem)


@app.route('/viagem/<viagem_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_viagem(viagem_id):
    viagem = Viagem.query.get(viagem_id)

    database.session.delete(viagem)
    database.session.commit()
    flash('Viagem Excluída', 'alert-danger')
    return redirect(url_for('usuarios'))


@app.route('/viagem/pesquisar', methods=['GET', 'POST'])
@login_required
def pesquisar_viagem():
    destino = request.args.get('destino', '')
    data_inicio = request.args.get('data_inicio', '')
    data_termino = request.args.get('data_termino', '')

    viagens = Viagem.query
    if destino:
        viagens = viagens.filter(Viagem.destino.ilike(f'%{destino}%'))
    if data_inicio:
        viagens = viagens.filter(Viagem.data_inicio >= data_inicio)
    if data_termino:
        viagens = viagens.filter(Viagem.data_termino <= data_termino)

    viagens = viagens.all()
    
    return render_template('pesquisar_viagem.html', viagens=viagens)
