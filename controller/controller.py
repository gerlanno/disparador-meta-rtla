import sys
import os
from urllib import response
from tqdm import tqdm
from requests import delete, session
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
)
from config.configs import dados_contas
from database.db import create_session
from sqlalchemy import text, update, select, delete, func
from utils.logger import Logger
from model.Models import (
    Cartorio,
    Titulo,
    Devedor,
    Contato,
    Zapenviado,
    Template,
    Wb_account,
)

logger = Logger().get_logger()


def processa_dados_titulo(dados):
    """
    Função que recebe os dados extraídos dos arquivos
    XML e processa o cadastro de cada componente.
    """
    session = create_session()
    try:

        ultimo_id_cadastrado = inserir_titulo(dados[0], session)

        for devedor in dados[1]:
            inserir_devedor(ultimo_id_cadastrado, devedor, session)

        if dados[2]:
            for contato in dados[2]:
                inserir_contato(contato, session)

    except Exception as e:
        logger.error(e)

    session.close()


def inserir_titulo(dados_titulo, session):
    """
    Função responsável por cadastrar os titulos.
    """
    campos = [
        "cartorio_id",
        "protocolo",
        "credor",
        "valorprotestado",
        "numerotitulo",
        "dataprotesto",
        "mesano",
        "valorboleto",
    ]

    # Definindo um dicionario com os campos e os dados recebidos por parametro
    data_dict = dict(zip(campos, dados_titulo))
    try:

        titulo = Titulo(**data_dict)
        session.add(titulo)
        session.commit()

        result = session.execute(text("SELECT lastval();"))
        last_inserted_id = result.scalar()

        return last_inserted_id

    except Exception as e:
        logger.error(e)


def inserir_devedor(id_titulo, dados_devedor, session):
    """
    Função responsável por cadastrar os devedores.
    """
    documento, nome = dados_devedor
    try:
        devedor = Devedor(titulo_id=id_titulo, documento=documento, nome=nome)
        session.add(devedor)
        session.commit()

    except Exception as e:
        logger.error(e)


def inserir_contato(dados_contato, session):
    """
    Função responsável por cadastrar os contatos dos devedores.

    """
    from src.sender import iswhatsapp

    documento, telefone = dados_contato
    # iswhats = iswhatsapp(telefone)
    try:
        contato = Contato(documento=documento, telefone=telefone)
        session.add(contato)
        session.commit()

    except Exception as e:
        session.rollback()
        logger.error(e)


def atualizar_contato():
    session = create_session()
    sucessos = 0
    erros = 0
    # Evitar erro de importação circular.
    from utils.tools import atualizar_whatsapp

    """
    Função responsável por atualizar os contatos dos devedores.
    """

    dados_contato = atualizar_whatsapp()

    if dados_contato:
        for dados in tqdm(
            dados_contato, "Atualizando..", unit="Contato", colour="BLUE"
        ):
            
            documento, telefone = dados

            try:
                if telefone[2] in ["8", "9"]:
                    whatsapp = f"55{telefone}"

                    query = (
                        session.query(Contato)
                        .filter(Contato.documento == documento)
                        .filter(Contato.telefone == "")
                        .all()
                    )
                    if len(query) > 0:

                        session.query(Contato).filter(
                            Contato.documento == documento
                        ).filter(Contato.telefone == "").update(
                            {Contato.telefone: whatsapp}
                        )
                        session.commit()
                    else:
                        contato = Contato(documento=documento, telefone=whatsapp)
                        session.add(contato)
                        session.commit()
                    sucessos = sucessos + 1
            except Exception as e:
                erros = erros + 1
                session.rollback()
                logger.error(str(e.args))

        return print(f"Atualização concluída. \nErros: {erros}\nSucesso: {sucessos}")


def titulos_registrados():
    """
    retona a quantidade de titulos existente no banco.
    """
    session = create_session()

    qtd_titulos = session.query(Titulo).all()

    session.close()

    return len(qtd_titulos)


def get_titulos(**kwargs):
    """
    Função para obter uma lista de titutlos que ainda não
    foi feita a comunicação.
    """

    lista_titulos = []
    session = create_session()

    # Consultar os ids que não estão na tabela zapenviados.
    zapenviado_filter = (
        session.query(Zapenviado.titulo_id)
        .filter(
            Zapenviado.titulo_id == Titulo.id,
            Zapenviado.mesano_insert == Titulo.mesano_insert,
        )
        .exists()
    )

    if kwargs:
        cartorio = kwargs.get("cartorio")
        # Filtragem de titulos por cartório
        mesano_filter = input("Filtrar por mesano_insert? ").strip()
        titulos_para_enviar = session.query(Titulo).filter(~zapenviado_filter)

        if mesano_filter:
            titulos_para_enviar = titulos_para_enviar.filter(
                Titulo.mesano_insert == mesano_filter
            )

        titulos_para_enviar = (
            titulos_para_enviar.filter(Titulo.cartorio_id == cartorio)
            .order_by(Titulo.valorprotestado)
            .all()
        )

    else:
        # Lista de titulos sem filtro de cartório, somente os que não foram enviados ainda.
        mesano_filter = input("Filtrar por mesano_insert? ").strip()
        titulos_para_enviar = session.query(Titulo).filter(~zapenviado_filter)
        if mesano_filter:
            titulos_para_enviar = titulos_para_enviar.filter(
                Titulo.mesano_insert == mesano_filter
            )
        titulos_para_enviar = (
            titulos_para_enviar.query(Titulo)
            .order_by(Titulo.valorprotestado).all()
        )

    for titulo in titulos_para_enviar:

        titulo_id = titulo.id
        numero_titulo = titulo.numerotitulo
        nome_credor = titulo.credor
        valor_titulo = str(titulo.valorprotestado)
        mesano_insert = titulo.mesano_insert
        url_cartorio, nome_cartorio = (
            session.query(Cartorio.website, Cartorio.nome)
            .filter(Cartorio.id == titulo.cartorio_id)
            .one()
        )

        devedores = (
            session.query(Devedor)
            .filter(
                Devedor.titulo_id == titulo.id,
                func.char_length(Devedor.documento) == 11,
            )
            .all()
        )

        telefone = []
        for devedor in devedores:

            documento = devedor.documento
            nome_devedor = devedor.nome
            contatos = (
                session.query(Contato.telefone)
                .filter(Contato.documento == devedor.documento)
                .filter(Contato.validado == True)
                .all()
            )

            for contato in contatos:
                # Limitar a 2 números por titulo.
                if len(telefone) < 2:
                    if len(contato.telefone) > 0:
                        telefone.append(contato.telefone)
                else:
                    pass

        if telefone:
            lista_titulos.append(
                (
                    nome_devedor,
                    titulo_id,
                    nome_credor,
                    valor_titulo,
                    numero_titulo,
                    mesano_insert,
                    url_cartorio,
                    nome_cartorio,
                    telefone if telefone else None,
                )
            )

    session.close()
    return lista_titulos if len(lista_titulos) > 0 else False


def titulos_para_enviar(**kwargs):
    # Retornar quantos titulos para disparar mensagens.
    if kwargs:
        titulos = get_titulos(cartorio=int(kwargs.get("cartorio")))
    else:
        titulos = get_titulos()
    if titulos:
        disparos = 0
        print(len(titulos))
        for titulo in titulos:
            disparos += len(titulo[8])
        return disparos
    else:
        return False


def cadastrar_template(**kwargs):
    """
    Função para cadastrar ou atualizar um template existente.
    """
    name = kwargs.get("name")
    status = kwargs.get("status")
    language = kwargs.get("language")
    wbaccount_id = kwargs.get("wbaccount_id")

    try:
        session = create_session()

        template = Template(**kwargs)

        session.add(template)

        session.commit()
        logger.info("Cadastro de templates concluído")
    except Exception as e:
        session.rollback()

        try:
            session.query(Template).filter(Template.name == name).filter(
                Template.wbaccount_id == wbaccount_id
            ).update({Template.status: status})
            session.commit()
            logger.info("Atualização de templates concluída.")
        except Exception as e:
            logger.error("Erro atualizando.. ", e)

    session.close()


def get_templates(business_acc_id):
    """
    Função para obter a lista de templates cadastradas no banco de dados.
    """
    session = create_session()
    list_templates = []
    try:
        query = (
            session.query(Template.name)
            .filter(Template.wbaccount_id == business_acc_id)
            .filter(Template.status == "APPROVED")
            .all()
        )
        for template in query:
            list_templates.append(str(template[0]))

    except Exception as e:
        logger.error("Erro recuperando templates", e)

    session.close()
    return list_templates


def cadastrar_business_account():
    """
    Inserir no databse as contas de whatsapp business e seus dados
    """
    lista = dados_contas()
    session = create_session()

    for item in tqdm(
        lista,
        desc="Cadastrando Whatsapp business account",
        unit="Contas",
        colour="GREEN",
    ):
        try:

            business_acc = Wb_account(**item)
            session.add(business_acc)
            session.commit()

        except Exception as e:
            logger.error(e)

    session.close()
    return print("Whatsapp Business Accounts Cadastradas")


def get_business_account(**kwargs):
    """
    Retorna os dados das contas de whatsapp business cadastradas.
    """

    session = create_session()
    if kwargs:
        account_name = kwargs.get("name")

        business_acc = (
            session.query(Wb_account).filter(Wb_account.name == account_name).all()
        )
    else:
        business_acc = session.query(Wb_account).all()
    accounts = []
    for acc in business_acc:
        accounts.append(
            {
                "name": acc.name,
                "phone_id": acc.phone_id,
                "business_account_id": acc.business_account_id,
                "verified_name": acc.verified_name,
                "display_phone_number": acc.display_phone_number,
            }
        )

    session.close()
    return accounts


def historico_disparos(**kwargs):
    """
    Atualiza a tabela de mensagens enviadas e seus status
    """
    messageid = kwargs.get("messageid")
    titulo_id = kwargs.get("titulo_id")
    mesano_insert = kwargs.get("mesano_insert")
    whatsapp = kwargs.get("whatsapp")
    wa_id = kwargs.get("wa_id")
    message_status = kwargs.get("message_status")
    accepted = kwargs.get("accepted")
    rejected = kwargs.get("rejected")
    response = kwargs.get("response")
    error = kwargs.get("error")

    try:
        session = create_session()

        disparo = Zapenviado(
            messageid=messageid,
            titulo_id=titulo_id,
            whatsapp=whatsapp,
            wa_id=wa_id,
            message_status=message_status,
            accepted=accepted,
            rejected=rejected,
            response=response,
            error=error,
            mesano_insert=mesano_insert,
        )

        session.add(disparo)

        session.commit()

    except Exception as e:
        logger.error(e)

        session.rollback()
    session.close()


def get_zapenviados():
    session = create_session()
    zapenviados = []
    historico_mensagens = session.query(Zapenviado).all()
    for mensagem in historico_mensagens:
        zapenviados.append(
            {
                "messageid": mensagem.messageid,
                "titulo_id": mensagem.titulo_id,
                "whatsapp": mensagem.whatsapp,
                "wa_id": mensagem.wa_id,
                "message_status": mensagem.message_status,
                "accepted": mensagem.accepted,
                "rejected": mensagem.rejected,
                "response": mensagem.response,
                "error": mensagem.error,
                "datainsert": str(mensagem.datainsert),
            }
        )

    return zapenviados


def del_zapfailed():
    import csv

    session = create_session()
    numbers = set()

    with open("delete_records_ok.csv", mode="r", encoding="utf-8") as arquivo_csv:
        try:
            count = 1
            reader = csv.reader(arquivo_csv)

            for row in reader:
                # for row in tqdm(reader,    "Processando arquivo CSV..", unit="Linhas"):
                numbers.add((row[0], row[2]))

        except Exception as e:
            logger.info("Erro", e)

    for number in tqdm(numbers, "delete records", colour="RED"):
        try:
            result = session.query(Zapenviado).filter_by(messageid=number[0]).first()
            if result:
                session.delete(result)
                session.commit()
            # session.query(Zapenviado).filter(Zapenviado.messageid==number[0]).filter(Zapenviado.whatsapp==number[1]).delete(synchronize_session=False)
            logger.info(f"Excluir registro: {number} - {result}")

        except Exception as e:
            session.rollback()
            logger.info(f"Erro - Excluir registro: - {e}")

    session.close()


def update_zapenviado():

    import csv

    with open("att_zapenviado.csv", mode="r", encoding="utf-8") as arquivo_csv:
        try:
            count = 1
            reader = csv.DictReader(arquivo_csv)

            for index, row in enumerate(reader):

                messageid = row.get("messageid")
                titulo_id = row.get("titulo_id")
                whatsapp = row.get("whatsapp")
                wa_id = row.get("wa_id")
                message_status = row.get("message_status")
                accepted = row.get("accepted")
                rejected = row.get("rejected")
                response = row.get("response")
                error = row.get("error")
                mesano_insert = row.get("mesano_insert")

                historico_disparos(
                    messageid=messageid,
                    titulo_id=int(titulo_id),
                    whatsapp=whatsapp,
                    wa_id=wa_id,
                    message_status=message_status,
                    response=response,
                    mesano_insert=mesano_insert,
                )

        except Exception as e:
            logger.info("Erro", e)


def att_iswhatsapp():
    from utils.tools import not_whatsapp

    lista_numeros = not_whatsapp()
    session = create_session()
    contatos = session.query(Contato).all()

    for numero in tqdm(lista_numeros, desc=f"Atualizando"):
        oito_ultimos_num = numero[-8:]
        try:

            session.query(Contato).filter(
                Contato.telefone.like(f"%{oito_ultimos_num}")
            ).update({Contato.validado: False})
            session.commit()
        except Exception as e:
            logger.error(f"Erro atualizando Telefone - {e}")
