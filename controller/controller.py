import sys
import os

from requests import session

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from database.db import create_session
from sqlalchemy import text, update
from model.Models import Cartorio, Titulo, Devedor, Contato, Zapenviado, Template, Wb_account



def processa_dados_titulo(dados):

    session = create_session()
    try:

        ultimo_id_cadastrado = insert_titulo(dados[0], session)

        for devedor in dados[1]:
            inserir_devedor(ultimo_id_cadastrado, devedor, session)

        if dados[2]:
            for contato in dados[2]:
                inserir_contato(contato, session)


    except Exception as e:
        print(e)

    session.close()


def insert_titulo(dados_titulo, session):
    
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

    data_dict = dict(zip(campos, dados_titulo))
    try:
        titulo = Titulo(**data_dict)
        session.add(titulo)
        session.commit()

        result = session.execute(text("SELECT lastval();"))    
        last_inserted_id = result.scalar()

        return last_inserted_id

    except Exception as e:
        pass   


def inserir_devedor(id_titulo, dados_devedor, session):
 
    documento, nome = dados_devedor
    try:
        devedor = Devedor(titulo_id=id_titulo, documento=documento, nome=nome)
        session.add(devedor)
        session.commit()        

    except Exception as e:
        pass
    

def inserir_contato(dados_contato, session):
 
    documento, telefone = dados_contato
    try:
        contato = Contato(documento=documento, telefone=telefone)
        session.add(contato)
        session.commit()

    except Exception as e:
        pass
    

def titulos_registrados():
    """
    retona a quantidade de titulos existente no banco.
    """
    session = create_session()

    qtd_titulos = session.query(Titulo).all()

    session.close()

    return len(qtd_titulos)


def get_titulos():
    
    session = create_session()
    titulos = session.query(Titulo).all()

    for titulo in titulos[:10]:
        
        # CHECA SE JÁ FOI FEITA A COMUNICAÇÃO DO TITULO ATUAL        
        enviado = session.query(Zapenviado.titulo_id).filter(Zapenviado.titulo_id == titulo.id).all()
        if len(enviado) > 0:
            print("Já foi")

        # EM CASO NEGATIVO, COLETAR AS INFORMAÇÕES PARA REALIZAR O DISPARO
        else:
            devedores = session.query(Devedor).filter(Devedor.titulo_id == titulo.id).all()

            for devedor in devedores:

                documento = devedor.documento
                
                contatos = session.query(Contato.telefone).filter(Contato.documento == devedor.documento).all()                      
                
                for contato in contatos:
                    # VERIFICAR SE EXISTE CONTATO CADASTRADO
                    if len(contato.telefone) > 0:
                        telefone = contato.telefone
                else:
                    pass


    session.close()


def cadastrar_template(**kwargs):

    name = kwargs.get("name")
    status = kwargs.get("status")
    language = kwargs.get("language")
    wbaccount_id = kwargs.get("wbaccount_id")
    
    try:
        session = create_session()

        template = Template(**kwargs)

        session.add(template)

        session.commit()
        
        
    except Exception as e:
        session.rollback()
        print(f"Erro cadastrando template: {e}")
        try:
            session.query(Template).filter(Template.name == name).filter(Template.wbaccount_id == wbaccount_id).update({Template.status: status})
            session.commit()
            print("Template atualizado")    
        except Exception as e:
            print("Erro atualizando.. ", e)

    session.close()


def get_business_account():
    session = create_session()

    business_acc = session.query(Wb_account).all()
    accounts = []
    for acc in business_acc:
        accounts.append({"name": acc.name,
               "phone_id": acc.phone_id, 
               "business_account_id": acc.business_account_id,
               "verified_name": acc.verified_name,
               "display_phone_number": acc.display_phone_number
               })
    return accounts



