from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Troque 'your_secret_key' por uma chave secreta forte
app.json.sort_keys = False

def ler_db(db):
    if not os.path.exists(db):
        return {db: []}
    with open(db, 'r', encoding='UTF-8') as arquivo:
        return json.load(arquivo)

def salvar_usuario(db):
    with open('db_user.json', 'w', encoding='UTF-8') as arquivo:
        json.dump(db, arquivo, indent=4)

def salvar_viagem(db):
    with open('db_travel.json', 'w', encoding='UTF-8') as arquivo:
        json.dump(db, arquivo, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET'])
def formulario_cadastro():
    return render_template('cadastro.html')

@app.route('/login', methods=['GET'])
def formulario_login():
    return render_template('login.html')

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    banco_dados = ler_db("db_user.json")
    return jsonify(banco_dados)

def verificao_de_login(email, senha):
    dados = ler_db("db_user.json")
    usuarios = dados.get("usuarios", [])

    for usuario in usuarios:
        if usuario["email"] == email and usuario["senha"] == senha:
            return True
    return False

@app.route('/login', methods=['POST'])
def endpoint_verificao_de_login():
    email = request.form.get("email")
    senha = request.form.get("senha")
    if not email or not senha:
        return jsonify({"erro": "Dados de login ausentes"}), 400  # Bad request
    if verificao_de_login(email, senha):
        # Definir a sessão do usuário
        session['user'] = email
        return redirect(url_for('welcome'))
    else:
        return jsonify({"erro": "Credenciais inválidas"}), 401

@app.route('/cadastro/usuarios', methods=['POST'])
def cadastrar_usuario():
    dados = request.form

    if not all(k in dados for k in ("nome", "email", "senha")):
        return jsonify({"erro": "Dados incompletos"}), 400

    nome = dados["nome"]
    email = dados["email"]
    senha = dados["senha"]

    banco_dados = ler_db("db_user.json")

    for usuario in banco_dados["usuarios"]:
        if usuario["email"] == email:
            return jsonify({"erro": "Email já cadastrado"}), 400

    novo_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha
    }
    banco_dados["usuarios"].append(novo_usuario)
    salvar_usuario(banco_dados)

    # Redirecionar para a página inicial após o cadastro
    return redirect(url_for('home'))

@app.route('/welcome', methods=['GET'])
def welcome():
    if 'user' not in session:
        return redirect(url_for('formulario_login'))
    return render_template('welcome.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('formulario_login'))

@app.route('/viagens', methods=['GET'])
def listar_viagens():
    banco_dados = ler_db("db_travel.json")
    return jsonify(banco_dados)

@app.route('/cadastro/viagens', methods=['POST'])
def cadastrar_viagens():
    dados = request.json

    if not all(k in dados for k in ("id", "destino", "data_inicio", "data_termino", "roteiro")):
        return jsonify({"erro": "Dados incompletos"}), 400

    id = dados["id"]
    destino = dados["destino"]
    data_inicio = dados["data_inicio"]
    data_termino = dados["data_termino"]
    roteiro = dados["roteiro"]

    banco_dados = ler_db("db_travel.json")

    nova_viagem = {
        "id": id,
        "destino": destino,
        "data_inicio": data_inicio,
        "data_termino": data_termino,
        "roteiro": roteiro
    }
    banco_dados["viagens"].append(nova_viagem)
    salvar_viagem(banco_dados)

    return jsonify({"mensagem": "Viagem cadastrada com sucesso!"}), 201

def atualizar_viagem(viagem_id, novos_dados):
    dados = ler_db("db_travel.json")
    viagens = dados.get("viagens", [])

    for viagem in viagens:
        if viagem["id"] == viagem_id:
            viagem.update(novos_dados)
            salvar_viagem(dados)
            return viagem
    return None

@app.route('/atualizar_viagem/<int:viagem_id>', methods=['PUT'])
def endpoint_atualizar_viagem(viagem_id):
    novos_dados = request.json
    viagem_atualizada = atualizar_viagem(viagem_id, novos_dados)
    if viagem_atualizada:
        return jsonify(viagem_atualizada), 200
    else:
        return jsonify({"erro": "Viagem não encontrada"}), 404

def deletar_viagem(viagem_id):
    dados = ler_db("db_travel.json")
    viagens = dados.get("viagens", [])

    for i, viagem in enumerate(viagens):
        if viagem["id"] == viagem_id:
            del viagens[i]
            salvar_viagem(dados)
            return viagem
    return None

@app.route('/deletar_viagem/<int:viagem_id>', methods=['DELETE'])
def endpoint_deletar_viagem(viagem_id):
    viagem_deletada = deletar_viagem(viagem_id)
    if viagem_deletada:
        return jsonify({"mensagem": "Viagem deletada com sucesso", "viagem": viagem_deletada}), 200
    else:
        return jsonify({"erro": "Viagem não encontrada"}), 404

def buscar_viagem_por_destino(destino):
    dados = ler_db("db_travel.json")
    viagens = dados.get("viagens", [])

    viagens_encontradas = [viagem for viagem in viagens if viagem.get("destino").lower() == destino.lower()]
    return viagens_encontradas

@app.route('/buscar_viagem', methods=['GET'])
def endpoint_buscar_viagem():
    destino = request.args.get('destino')
    if destino:
        viagens_encontradas = buscar_viagem_por_destino(destino)
        if viagens_encontradas:
            return jsonify(viagens_encontradas), 200
        else:
            return jsonify({"erro": "Nenhuma viagem encontrada para o destino especificado"}), 404
    else:
        return jsonify({"erro": "Destino não especificado"}), 400

if __name__ == '__main__':
    app.run(debug=True)
