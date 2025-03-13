import json
import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "."))
)

from src.data.extract_data import extrair_dados
from flask import Flask, jsonify, request 



app = Flask(__name__)


@app.route("/")
def index():
    return jsonify({"status": "sucess"}), 200



@app.route("/extrair", methods=["GET"])
def extract_view():
    response = extrair_dados()

    if response.get("sucess") == True:
        return jsonify({"sucess": True}), 200
    else:
        return jsonify({"sucess": False}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)