import sys
import os
import requests
import json
from xml.dom import NotFoundErr
from tqdm import tqdm
from itertools import islice

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from controller.controller import (
    get_titulos,
    get_business_account,
    get_templates,
    historico_disparos,
    cadastrar_template,
)
from config.configs import find_token
from utils.tools import convert_to_brl
from utils.logger import Logger
from time import sleep


logger = Logger().get_logger()


template_name = ""

def parse_error(response_text):
    error = response_text.get("error", {})
    if error:
        error_message = error.get("message", "Erro desconhecido")
        error_code = error.get("code", "Sem código")
        return str(error_code), str(error_message)
    return None


def parse_response(response_text):
    # Inicializando variáveis com None como padrão
    message_status = None
    message_id = None
    wa_id = None

    try:

        messages = response_text.get("messages", [])
        if messages and isinstance(messages, list):
            message_status = messages[0].get("message_status")
            message_id = messages[0].get("id")

        contacts = response_text.get("contacts", [])
        if contacts and isinstance(contacts, list):
            wa_id = contacts[0].get("wa_id")

    except (IndexError, KeyError, TypeError) as e:
        print(f"Erro ao processar a resposta: {e}")

    return message_status, message_id, wa_id


def set_template(business_id):

    list_templates = get_templates(business_id)

    for template in list_templates:
        if "cancelamento" in template:
            global template_name
            template_name = template
            return template_name

    raise NotFoundErr


def disparar(business_acc_name, qtd_disparos):

    # Buscar a conta da meta informada.
    accounts = get_business_account(name=business_acc_name)
    for acc in accounts:
        business_id = acc.get("business_account_id")
        phone_id = acc.get("phone_id")
        api_token = find_token(phone_id)

    # Buscar um template
    try:
        global template_name
        template_name = set_template(business_id)

    except Exception as e:
        print("Não foram encontrados templates para operação de cancelamento")

    # Buscar a lista de titulos
    if business_acc_name in ["AGUIAR1", "AGUIAR2"]:
        titulos = get_titulos(cartorio=8)
    elif business_acc_name in ["OSSIAN1", "OSSIAN2"]:
        titulos = get_titulos(cartorio=5)
    else:
        titulos = get_titulos()

    # Se não for informado a quantidade total de disparos, disparar todos os titulos retornados.
    qtd_disparos = qtd_disparos if qtd_disparos else len(titulos)

    if titulos and template_name:
        for titulo in tqdm(
            islice(titulos, qtd_disparos),
            total=qtd_disparos,
            desc="Iniciando disparos..",
            unit="Disparos ",
            colour="GREEN",
        ):
            (
                nome_devedor,
                titulo_id,
                nome_credor,
                valor_titulo,
                numero_titulo,
                mesano_insert,
                url_cartorio,
                nome_cartorio,
                telefones,
            ) = titulo

            # parametros do template de cancelamento
            paramentros_template = [
                {
                    "type": "text",
                    "text": nome_devedor,
                },
                {
                    "type": "text",
                    "text": nome_credor,
                },
                {
                    "type": "text",
                    "text": convert_to_brl(valor_titulo),
                },
                {
                    "type": "text",
                    "text": numero_titulo,
                },
                {
                    "type": "text",
                    "text": url_cartorio,
                },
                {
                    "type": "text",
                    "text": nome_cartorio,
                },
            ]

            
            for telefone in telefones:                
                # Enviar a mensagem para o número de cadastro do titulo.
                send_messages(
                    phone_id,
                    api_token,
                    telefone,
                    template_name,
                    titulo_id,
                    mesano_insert,
                    paramentros_template,
                    business_id,
                )

    else:
        return {"Status": "Nada a processar"}

    return {"Status": True}

def send_messages(
    phone_id,
    api_token,
    telefone,
    template,
    titulo_id,
    mesano_insert,
    paramentros_template,
    business_id,
):

    # URL da API
    api_url = f"https://graph.facebook.com/v20.0/{phone_id}/messages"

    # Cabeçalhos da solicitação
    headers = {
        f"Authorization": api_token,  # token de acesso do cartório informado
        "Content-Type": "application/json",
    }

    # Corpo da mensagem
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"{telefone}",
        "type": "template",
        "template": {
            "name": f"{template}",
            "language": {"code": "pt_BR"},
            "components": [
                {
                    "type": "body",
                    "parameters": paramentros_template,
                }
            ],
        },
    }

    response = requests.request(method="POST", url=api_url, headers=headers, json=data)
    response_text = json.loads(response.text)
    status_code = response.status_code
    logger.info(response_text)

    if status_code == 200:
        message_status, messageid, wa_id = parse_response(response_text)
        # Gravar a mensagem enviada no banco
        historico_disparos(
            messageid=messageid,
            titulo_id=int(titulo_id),
            mesano_insert=mesano_insert,
            whatsapp=telefone,
            wa_id=wa_id,
            message_status=message_status,
            response=str(response_text),
        )

    else:

        error_code, error_message = parse_error(response_text)

        # Grava erros no log.
        logger.error(
            f"Titulo id: {titulo_id}; Whatsapp: {telefone}; Error Code: {error_code}; Error message: {error_message}; Response Text: {str(response_text)}"
        )

        # Verifica se foi erro de template.
        if error_code in ["132015", "132016"]:

            logger.info("Erro no template!")
            # Caso dê erro no template, desativar o mesmo, e selecionar um outro.

            cadastrar_template(
                name=template, wbaccount_id=business_id, status="DISABLED"
            )

            # Atualizar o template e reenviar a mensagem.
            global template_name
            template_name = set_template(business_id)
            send_messages(
                phone_id,
                api_token,
                telefone,
                template_name,
                titulo_id,
                paramentros_template,
                business_id,
            )
