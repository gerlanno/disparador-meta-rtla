import os
from dotenv import load_dotenv



load_dotenv()

# nome do cartorio e código do cartorio
PRIMEIRO_CARTORIO_DE_FORTALEZA = "1"
OSIAN_ARARIPE = "5"
CARTORIO_AGUIAR = "8"

db_config = {
    "host": "localhost",
    "database": "pyextractdb",
    "user": "pyextractdb",
    "password": os.getenv("DB_PG_PASS"),
}


mail_config = {
    "user": "gerlannoservis@gmail.com",
    "password": os.getenv("GMAIL_PASS"),
    "host": "imap.gmail.com",
}

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
    for item in wa_config.values():
        if item.get("PHONE_NUMBER_ID") == phone_number_id:

            token_found = item.get("WA_TOKEN")

            break
        else:
            token_found = ""
    return token_found if token_found else print("Token não localizado")
