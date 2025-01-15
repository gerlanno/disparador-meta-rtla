from email import message_from_file
import sys
import os
import csv
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from controller.controller import get_zapenviados
from utils.logger import Logger
from src.data.extract_data import AGORA
from tqdm import tqdm
logger = Logger().get_logger()

def convert_to_brl(value):

    """
    Converter e formatar valores para o formato de moeda Real do Brasil.
    """
    value_brl = (
        (
            f"R$ {float(value.replace(',','').replace('.', ''))/100:_.2f}"
        )
        .replace(".", ",")
        .replace("_", ".")
    )

    return value_brl

def zapeviados_to_csv():
    """
    Salvar registros da tabela zapenviados para csv
    """
    message_list = get_zapenviados()
 
    with open(f"sendhistory-{AGORA}.csv", mode='w', newline='', encoding='utf-8') as arquivo_csv:
        try:
            fieldnames = message_list[0].keys()
            writer = csv.DictWriter(arquivo_csv, fieldnames=fieldnames)
            writer.writeheader()

            for row in tqdm(message_list, desc="Escrevendo CSV", unit="Linha"):
                writer.writerow(row)

            print("Exportação concluída.")
        except Exception as e:
            print("Erro, ver aquivo de logs para mais detalhes.")
            logger.info("Erro", e)


