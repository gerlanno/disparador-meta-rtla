import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytz
from schedule import every, run_pending
from time import sleep
import schedule
import requests

from datetime import datetime


API_URL = "http://localhost:5001/"

ENDPOINT_EXTRAIR = 'extrair'
ENDPOINT_DISPARO = 'disparo'

def job():
    from model.Models import Agendamentos, create_session
    session = create_session()
    agendamentos = session.query(Agendamentos).filter(Agendamentos.data_disparo == HOJE.strftime("%Y-%m-%d")).all()

    ###################### ALTERAÇOES PARA FAZER ######################
    # MUDAR O STATUS NA TABELA DE AGENDAMENTOS QUANDO O DISPARO FOR FEITO
    # ACRESCENTAR O FILTRO DE STATUS JUNTO COM O DA DATA


    if agendamentos:        
        for agendamento in agendamentos:
            payload = {"id_agendamento": agendamento.id, "arquivo": agendamento.nome_arquivo}
            
            response = requests.get(API_URL+ENDPOINT_EXTRAIR, params=payload)
            print(payload)
    else:        
        print(f"Sem agendamentos para hoje: {HOJE.strftime("%Y-%m-%d")}")

    response = requests.get(API_URL+ENDPOINT_DISPARO)

schedule.every().monday.at("09:00", 'America/Sao_Paulo').do(job)
schedule.every().tuesday.at("09:00", 'America/Sao_Paulo').do(job)
schedule.every().wednesday.at("09:00", 'America/Sao_Paulo').do(job)
schedule.every().thursday.at("09:00", 'America/Sao_Paulo').do(job)
schedule.every().friday.at("12:20" \
"", 'America/Sao_Paulo').do(job)


while 1:
   
    n = schedule.idle_seconds()

    if n == None:
        print("No more jobs")
        break
    elif n > 0 :
        print(f"Sleeping {n} seconds before next job")
        sleep(n)    
 
    HOJE = datetime.now() 
    
    schedule.run_pending()
