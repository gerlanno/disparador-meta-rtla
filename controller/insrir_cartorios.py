from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import  create_engine
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.Models import Cartorio

from database.db import create_session

def dados_cartorio():
    session = create_session()

    cartorios = session.query(Cartorio.id).all()

    if len(cartorios) > 0:
        ...
    else:    
        cartorio1 = Cartorio(id=1, nome='1o Ofício de Notas e Protesto', website='https://1cartoriodefortaleza.com.br/')
        cartorio2 = Cartorio(id=5, nome='Cartório Ossian Araripe', website='https://www.cartorioossianararipe.com.br/')
        cartorio3 = Cartorio(id=8, nome='Cartório Aguiar', website='https://www.cartorioaguiar.com.br/')

        cartorios = [cartorio1, cartorio2, cartorio3]
        try:
            session.add_all(cartorios)

            session.commit()
            session.close()

        except Exception as e:
            session.rollback()
            print("Erro: ", e)

        return print("Dados dos cartórios registrados.")

