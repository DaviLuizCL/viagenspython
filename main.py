from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

CAMINHO_ARQUIVO = 'db.json'

def ler_banco_dados():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return {"usuarios": []}
    with open(CAMINHO_ARQUIVO, 'r') as arquivo:
        return json.load(arquivo)

def salvar_banco_dados(banco_dados):
    with open(CAMINHO_ARQUIVO, 'w') as arquivo:
        json.dump(banco_dados, arquivo, indent=4)

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    banco_dados = ler_banco_dados()
    return jsonify(banco_dados)

@app.route('/cadastro/usuarios', methods=['POST'])
def cadastrar_usuario():
    dados = request.json

    if not all(k in dados for k in ("nome", "email", "senha")):
        return jsonify({"erro": "Dados incompletos"}), 400

    nome = dados["nome"]
    email = dados["email"]
    senha = dados["senha"]

    banco_dados = ler_banco_dados()

    for usuario in banco_dados["usuarios"]:
        if usuario["email"] == email:
            return jsonify({"erro": "Email já cadastrado"}), 400

    novo_usuario = {
        "nome": nome,
        "email": email,
        "senha": senha
    }
    banco_dados["usuarios"].append(novo_usuario)
    salvar_banco_dados(banco_dados)

    return jsonify({"mensagem": "Usuário cadastrado com sucesso"}), 201

@app.route('/viagens', methods=['GET'])
def listar_viagens():
    banco_dados = ler_banco_dados()
    return jsonify(banco_dados["viagens"])

@app.route('/cadastro/viagens', methods=['POST'])
def cadastrar_viagens():
    dados = request.json

    if not all(k in dados for k in ("destino", "data_inicio", "data_termino", "roteiro")):
        return jsonify({"erro": "Dados incompletos"}), 400

    destino = dados["destino"]
    data_inicio = dados["data_inicio"]
    data_termino = dados["data_termino"]
    roteiro = dados["roteiro"]

    banco_dados = ler_banco_dados()

    nova_viagem = {
        "destino": destino,
        "data_inicio": data_inicio,
        "data_termino": data_termino,
        "roteiro": roteiro
    }
    banco_dados["viagens"].append(nova_viagem)
    salvar_banco_dados(banco_dados)

    return jsonify({"mensagem": "Viagem cadastrado com sucesso!"}), 201

if __name__ == '__main__':
    app.run(debug=True)