from flask import Flask, render_template, request, redirect, url_for

from db_connection import create_connection, insert_user, insert_travel
import os
app = Flask(__name__)
print(os.getcwd())
print(os.listdir())
#Começando bem
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/viagens')
def register_travel():
    return render_template('register_travel.html')


@app.route('/registrar', methods=['GET', 'POST'])
def user():
    error_message = None
    if request.method == 'POST':
        nome = request.form['name']
        email = request.form['email']
        senha = request.form['password']
        confirmar_senha = request.form['confirm-password']

        if senha != confirmar_senha:
            error_message = 'As senhas não correspondem. Tente novamente.'
            return render_template('register_user.html', error_message=error_message)

        if insert_user(nome, email, senha):
            return redirect(url_for('index'))
        else:
            error_message = "Erro ao registrar o usuario, tente novamente mais tarde"

        # Processamento dos dados do formulário (ex.: salvar no banco de dados)
        print(f"Nome: {nome}")
        print(f"Email: {email}")
        print(f"Senha: {senha}")
        print(f"Confirmar Senha: {confirmar_senha}")

        return redirect(url_for('index'))

    return render_template('register_user.html', error_message=error_message)

@app.route('/viagens', methods=['GET', 'POST'])
def travel_register():
    error_message = None
    if request.method == 'post':
        destino = request.form['destination']
        data_partida = request.form['departure-date']
        data_retorno = request.form['return-date']
        numero_de_pessoas = request.form['number-of-people']
        descricao = request.form['description']

        if insert_travel(destino, data_partida, data_retorno, numero_de_pessoas, descricao):
            return redirect(url_for('index'))
        else:
            error_message = "Erro ao registrar o viagem, tente novamente mais tarde"
            
        print(f"Destino: {destino}")
        print(f"Data de partida: {data_partida}")
        print(f"Data de retorno: {data_retorno}")
        print(f"Número de pessoas: {numero_de_pessoas}")
        print(f"Descrição : {descricao}")

        return redirect(url_for('index'))
    
    return render_template('register_travel.html', error_message=error_message)


create_connection()
if __name__ == '__main__':
    app.run(debug=True)
