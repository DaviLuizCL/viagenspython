from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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

        # Processamento dos dados do formulário (ex.: salvar no banco de dados)
        print(f"Nome: {nome}")
        print(f"Email: {email}")
        print(f"Senha: {senha}")
        print(f"Confirmar Senha: {confirmar_senha}")

        return redirect(url_for('index'))

    return render_template('register_user.html', error_message=error_message)


if __name__ == '__main__':
    app.run(debug=True)
