import os
from dotenv import load_dotenv

load_dotenv()

# nome do cartorio e código do cartorio
PRIMEIRO_CARTORIO_DE_FORTALEZA = "1"
OSIAN_ARARIPE = "5"
CARTORIO_AGUIAR = "8"

# Banco de dados
db_config = {
    "host": os.getenv("dbhost"),
    "port": os.getenv("dbport"),
    "database": os.getenv("dbname"),
    "user": os.getenv("dbuser"),
    "password": os.getenv("dbpass"),
}
OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")
# Diretório com os arquivos para extração de dados.


UPLOADS_DIR = os.getenv("FILES_DIR") #PASTA PRA INTEGRAÇÃO COM O APP FLASK - NAO USADO

BASE_DIR = os.getcwd()
FILES_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(FILES_DIR, 'processed')
LOG_DIR = os.path.join(BASE_DIR, 'logs')


# Dados Whatsapp Business
wa_config = {
    "OSIAN1": {
        "NOME": "OSIAN ARARIPE",
        "WA_TOKEN": os.getenv("OSIAN_TOKEN"),
        "PHONE_NUMBER_ID": os.getenv(
            "OSIAN1_PHONE_NUMBER_ID"
        ),  # "display_phone_number": "+55 85 8663-3919"
    },
    "OSIAN2": {
        "NOME": "OSIAN ARARIPE",
        "WA_TOKEN": os.getenv("OSIAN_TOKEN"),
        "PHONE_NUMBER_ID": os.getenv(
            "OSIAN2_PHONE_NUMBER_ID"
        ),  # "display_phone_number": "+55 85 8663-2161"
    },
    "AGUIAR1": {
        "NOME": "CARTORIO AGUIAR",
        "WA_TOKEN": os.getenv("AGUIAR_TOKEN"),
        "PHONE_NUMBER_ID": os.getenv(
            "AGUIAR1_PHONE_NUMBER_ID"
        ),  # "display_phone_number": "+55 85 9759-0064"
    },
    "AGUIAR2": {
        "NOME": "CARTORIO AGUIAR",
        "WA_TOKEN": os.getenv("AGUIAR_TOKEN"),
        "PHONE_NUMBER_ID": os.getenv(
            "AGUIAR2_PHONE_NUMBER_ID"
        ),  # "display_phone_number": "+55 85 9412-9614"
    },
    "IEPTBCE1": {
        "NOME": "Instituto de Cartórios de Protestos do Ceará - IEPTBCE",
        "WA_TOKEN": os.getenv("IEPTBCE_TOKEN"),
        "PHONE_NUMBER_ID": os.getenv(
            "IEPTBCE1_PHONE_NUMBER_ID"
        ),  # "display_phone_number": "+55 85 9841-1019"
    },
    "IEPTBCE2": {
        "NOME": "Instituto de Cartórios de Protestos do Ceará - IEPTBCE",
        "WA_TOKEN": os.getenv("IEPTBCE_TOKEN"),
        "PHONE_NUMBER_ID": os.getenv(
            "IEPTBCE2_PHONE_NUMBER_ID"
        ),  # "display_phone_number": "+55 85 8217-5611"
    },
    "IEPTBCE3": {
        "NOME": "Instituto de Cartórios de Protestos do Ceará - IEPTBCE",
        "WA_TOKEN": os.getenv("IEPTBCE_TOKEN"),
        "PHONE_NUMBER_ID": os.getenv(
            "IEPTBCE3_PHONE_NUMBER_ID"
        ),  # "display_phone_number": "+55 85 9936-6186"
    },
    "RTLA1": {
        "NOME": "Instituto de Cartórios de Protestos do Ceará - IEPTBCE",
        "WA_TOKEN": os.getenv("RTLA_TOKEN"),
        "PHONE_NUMBER_ID": os.getenv(
            "RTLA1_PHONE_NUMBER_ID"
        ),  # "display_phone_number": "+55 85 9841-1242"
    },
    "RTLA2": {
        "NOME": "Instituto de Cartórios de Protestos do Ceará - IEPTBCE",
        "WA_TOKEN": os.getenv("RTLA_TOKEN"),
        "PHONE_NUMBER_ID": os.getenv(
            "RTLA2_PHONE_NUMBER_ID"
        ),  # "display_phone_number": "+55 85 9841-1052"
    },
}


def find_token(phone_number_id):

    """
    Localizar o token pelo phone number id.
    """
    for item in wa_config.values():
        if item.get("PHONE_NUMBER_ID") == phone_number_id:

            token_found = item.get("WA_TOKEN")

            break
        else:
            token_found = ""
    return token_found if token_found else print("Token não localizado")

def dados_contas():
    
    dados = [
        {
            "name": "AGUIAR1",
            "phone_id": "214744335057692",
            "business_account_id": "208428645692302",
            "verified_name": "Cartório Aguiar",
            "display_phone_number": "558594129614"
        },
        {
            "name": "AGUIAR2",
            "phone_id": "145717898625245",
            "business_account_id": "150991778095452",
            "verified_name": "Cartório Aguiar",
            "display_phone_number": "558597590064"
        },
        {
            "name": "OSSIAN1",
            "phone_id": "130290610176023",
            "business_account_id": "151660654694197",
            "verified_name": "Cartório Ossian Araripe",
            "display_phone_number": "558586633919"
        },
        {
            "name": "OSSIAN2",
            "phone_id": "140714015796020",
            "business_account_id": "105202826019315",
            "verified_name": "Cartório Ossian Araripe",
            "display_phone_number": "558586632161"
        },
        {
            "name": "IEPTB1",
            "phone_id": "106462279201071",
            "business_account_id": "106307439216846",
            "verified_name": "Ieptbce",
            "display_phone_number": "558582175611"
        },
        {
            "name": "IEPTB2",
            "phone_id": "101190366397218",
            "business_account_id": "101352253047460",
            "verified_name": "Ieptbce",
            "display_phone_number": "558598411019"
        },
        {
            "name": "IEPTB3",
            "phone_id": "261216513749428",
            "business_account_id": "231484600058458",
            "verified_name": "IEPTBCE",
            "display_phone_number": "558599366186"
        },
        {
            "name": "RTLA1",
            "phone_id": "115891571590409",
            "business_account_id": "114158791765127",
            "verified_name": "Ieptbce",
            "display_phone_number": "558598411052"
        },
        {
            "name": "RTLA2",
            "phone_id": "105309195992923",
            "business_account_id": "112070761975997",
            "verified_name": "Ieptbce",
            "display_phone_number": "558598411242"
        }
    ]
    return dados