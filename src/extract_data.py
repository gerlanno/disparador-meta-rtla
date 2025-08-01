import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
)
from venv import logger
import xml.etree.ElementTree as et
from tqdm import tqdm
from controller.controller import processa_dados_titulo, titulos_registrados
from datetime import datetime, tzinfo
from config.configs import (
    FILES_DIR,
    PROCESSED_DIR,
    UPLOADS_DIR,
    BASE_DIR,
    FILES_DIR,
    LOG_DIR,
)
from shutil import move

# Momento atual, com data e hora completa,
# será usado para renomear o arquivo processado.
AGORA = datetime.ctime(datetime.now()).replace(":", "").replace(" ", "")


def extract_cancelamento(file):
    """
    Extrair e tratar os dados do arquivo de cancelamento,
    chamar a função responsável por inseri-los no banco de dados.
    """
    arquivo = et.parse(file)
    root = arquivo.getroot()
    cartorio = root.find("cartorio")
    titulos = root.find("titulos")

    lista_titulos = []

    lista_geral = []

    for i, titulo in enumerate(titulos.findall("titulo")):

        # Extrair as informações do titulo
        cartorio_id = int(cartorio.find("codigo").text.strip())
        protocolo = titulo.find("protocolo").text.strip()
        credor = titulo.find("credor").text.strip().strip()
        valorprotestado = float((titulo.find("valorprotestado").text).replace(",", "."))
        numerotitulo = titulo.find("numerotitulo").text.strip()
        dataprotesto = titulo.find("dataprotesto").text
        mesano = dataprotesto[0:-2].replace("-", "")
        valorboleto = float((titulo.find("valorboleto").text))

        # Extrair informações dos devedores
        devedores = titulo.find("devedores")

        # Reiniciando a lista de devedores e telefone a cada titulo
        lista_devedores = []
        lista_contatos = []

        for devedor in devedores.findall("devedor"):

            nome_devedor = devedor.find("nome").text.strip()
            documento_devedor = (
                devedor.find("documento")
                .text.replace(".", "")
                .replace("/", "")
                .replace("-", "")
            )

            # Extrair os contatos dos devedores
            telefones = devedor.find("telefones")
            for telefone in telefones.findall("telefone"):

                whatsapp = ""
                if not telefone.text == None and telefone.text.isnumeric():
                    if telefone.text[2] != "3":
                        whatsapp = f"55{telefone.text}"

                        lista_contatos.append((documento_devedor, whatsapp))

            lista_devedores.append((documento_devedor, nome_devedor))
        lista_titulos.append(
            (
                cartorio_id,
                protocolo,
                credor,
                valorprotestado,
                numerotitulo,
                dataprotesto,
                mesano,
                valorboleto,
            )
        )

        """
        Uma lista geral para guardar os dados de 
        contato e devedores para cada titulo
        """
        lista_geral.append((lista_titulos[i], lista_devedores, lista_contatos))

    for index, titulo in enumerate(
        tqdm(lista_geral, desc="Processando dados", unit="Registro", colour="BLUE")
    ):

        if index == 0:
            num_inicial = titulos_registrados()

        processa_dados_titulo(titulo)

        if index + 1 == len(lista_geral):
            num_final = titulos_registrados()
            print(
                f"\nQuantidade total de titulos processados: {len(lista_geral)}\n Quantidade total de titulos registrados: {num_final - num_inicial}"
            )


# Itera pelos arquivos da pasta data, procurando pela lista de cancelamento.
def extrair_dados(folder=FILES_DIR):
    # DATA_FOLDER = r'{0}'.format(folder) - OBSOLETO
    sucess = 0

    for root, dirs, files in os.walk(FILES_DIR):
        if not "processed" in root:
            for file in files:
                
                if "Cancelamento" in file and file.endswith(".xml"):

                    file_path = os.path.join(root, file)

                    if os.path.isfile(os.path.join(PROCESSED_DIR, file)):

                        print(f"O arquivo [{file}] já foi importado anteriormente!")
                        logger.error(f"Arquivo já importado anteriormente - [{file}]")
                        
                    else:
                        extract_cancelamento(file_path)
                        # new_filename = f"Processado{AGORA}_{sucess}.xml"

                        path_processed = os.path.join(PROCESSED_DIR, file)

                        move(file_path, path_processed)

                        # os.rename(file_path, os.path.join(root, new_filename))
                        sucess = sucess + 1
                else:
                    return "Nada para importar!"

    if not sucess > 0:
        return {"sucess": False, "message": "Nenhum arquivo processado."}
    else:
        return {
            "sucess": True,
            "message": f"Tarefa concluída, arquivos processados: {sucess}.",
        }


