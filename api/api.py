import json
from re import X
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "."))
)

from src.data.extract_data import extrair_dados
from src.sender import disparar
from config.configs import FILES_DIR
from flask import Flask, jsonify, request
from controller.controller import *


app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"status": "sucess"}), 200


@app.route("/extrair", methods=["GET"])
def extract_view():

    response = extrair_dados(folder=FILES_DIR)

    if response.get("sucess") == True:
        return jsonify({"sucess": True}), 200
    else:
        return jsonify({"sucess": False}), 200


@app.route("/disparo/<cartorio_id>")
def disparo(cartorio_id):

    to_send = titulos_para_enviar(cartorio=cartorio_id)
    cartorio_id = int(cartorio_id)
    
    if to_send:

        # Divisão evitando números quebrados.
        conta_A = to_send // 2 if to_send % 2 == 0 else ((to_send - 1) // 2)
        conta_b = to_send // 2 if to_send % 2 == 0 else (to_send // 2) + 1
        qtd_disparos = [conta_A, conta_b]

        if cartorio_id == 5:
            business_acc_names = ["OSSIAN1", "OSSIAN2"]
            for i, acc in enumerate(business_acc_names):
                try:
                    disparar(acc, qtd_disparos=qtd_disparos[i])

                except Exception as e:
                    return jsonify({"error": e}), 500

        elif cartorio_id == 8:
            business_acc_names = ["AGUIAR1", "AGUIAR2"]
            for i, acc in enumerate(business_acc_names):
                try:
                    disparar(acc, qtd_disparos=qtd_disparos[i])

                except Exception as e:
                    error = jsonify({"error": e}), 500
        else:
            return jsonify({"error": "Cartório inválido"})

    return jsonify({"to_send": to_send if to_send else None})

@app.route("/to-send/<id>")
def to_send(cartorio_id):

    to_send = titulos_para_enviar(cartorio=cartorio_id)
    
    return jsonify({"Cartório": cartorio_id,
                    "a_disparar": to_send})



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
