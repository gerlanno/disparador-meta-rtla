import sys
import os
from urllib import response
from tqdm import tqdm
from requests import session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.configs import dados_contas

from database.db import create_session
from sqlalchemy import text, update
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
    documento, telefone = dados_contato
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
        for dados in tqdm(dados_contato, "Atualizando..", unit="Contato", colour="BLUE"):
            documento, telefone = dados
        
            if telefone[2] in ["8" , "9"]:
                whatsapp = f"55{telefone}"
                try:
                    query = session.query(Contato).filter(Contato.documento == documento).filter(Contato.telefone == "").all()
                    if len(query) > 0: 

                        session.query(Contato).filter(Contato.documento == documento).filter(Contato.telefone == "").update({Contato.telefone: whatsapp})
                        session.commit()
                    else:
                        contato = Contato(documento=documento, telefone=whatsapp)
                        session.add(contato)
                        session.commit()                  
                    sucessos = sucessos + 1
                except Exception as e:
                    erros = erros + 1
                    session.rollback()
                    logger.error(str(e))

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
    if kwargs:
        cartorio = kwargs.get("cartorio")
        titulos = session.query(Titulo).filter(Titulo.cartorio_id == cartorio).all()
    else:
        titulos = session.query(Titulo).all()

    for titulo in titulos:

        # CHECA SE JÁ FOI FEITA A COMUNICAÇÃO DO TITULO ATUAL
        enviado = (
            session.query(Zapenviado.titulo_id)
            .filter(Zapenviado.titulo_id == titulo.id)
            .all()
        )

        if len(enviado) > 0:
           ...

        # EM CASO NEGATIVO, COLETAR AS INFORMAÇÕES PARA REALIZAR O DISPARO
        else:
            titulo_id = titulo.id
            numero_titulo = titulo.numerotitulo
            nome_credor = titulo.credor
            valor_titulo = str(titulo.valorprotestado)
            url_cartorio = (
                session.query(Cartorio.website)
                .filter(Cartorio.id == titulo.cartorio_id)
                .one()
            )
            nome_cartorio = (
                session.query(Cartorio.nome)
                .filter(Cartorio.id == titulo.cartorio_id)
                .one()
            )

            devedores = (
                session.query(Devedor).filter(Devedor.titulo_id == titulo.id).all()
            )
            telefone = []
            for devedor in devedores:

                documento = devedor.documento
                nome_devedor = devedor.nome
                contatos = (
                    session.query(Contato.telefone)
                    .filter(Contato.documento == devedor.documento)
                    .all()
                )

                for contato in contatos:
                    # VERIFICAR SE EXISTE CONTATO CADASTRADO
                    if len(contato.telefone) > 0:
                        telefone.append(contato.telefone)
                else:
                    pass
            lista_titulos.append(
                (
                    nome_devedor,
                    titulo_id,
                    nome_credor,
                    valor_titulo,
                    numero_titulo,
                    url_cartorio[0],
                    nome_cartorio[0],
                    telefone if telefone else None,
                )
        )
    session.close()        
    return lista_titulos if len(lista_titulos) > 0 else False
    


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

    for item in tqdm(lista, desc="Cadastrando Whatsapp business account", unit="Contas", colour="GREEN"):
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
        name = kwargs.get("name")
        
        business_acc = (
            session.query(Wb_account)
            .filter(Wb_account.name == kwargs.get("name"))
            .all()
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
        zapenviados.append({
            "messageid": mensagem.messageid,
            "titulo_id": mensagem.titulo_id,
            "whatsapp": mensagem.whatsapp,
            "wa_id": mensagem.wa_id,
            "message_status": mensagem.message_status,
            "accepted": mensagem.accepted,
            "rejected": mensagem.rejected,
            "response": mensagem.response,
            "error": mensagem.error,
            "datainsert": str(mensagem.datainsert)   
        })
    
    return zapenviados