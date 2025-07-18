import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
)
from config.configs import OPENAI_APIKEY
from tqdm import tqdm
import time
from openai import OpenAI
from database.db import create_session
from sqlalchemy import select, update, insert, text

session = create_session()

from datetime import datetime

hoje = datetime.now().strftime("%Y-%m-%d")


client = OpenAI(api_key=OPENAI_APIKEY)

prompt = """
                    #Você é responsável por analisar as respostas recebidas em mensagens enviadas via WhatsApp pela empresa. Seu objetivo é identificar se a mensagem foi enviada para o número errado, com base na resposta recebida do destinatário.

                    ##Você receberá uma entrada no seguinte formato:
                    
                    "telefone": "5585992058133",
                    "message": "ola este numero nao me pertence, favor retirar da sua lista"
                    
                    ##Um duplo pipe '||' significa um separador de mensagens recebidas, para melhor contexto.  

                    ##Após analisar o conteúdo da mensagem, retorne:
                    - False se identificar que a resposta indica claramente que a mensagem foi enviada para a pessoa errada (por exemplo: "este número não me pertence", "mensagem errada", "não sou essa pessoa", "SAIR", retire meu nome da sua base de dados, isso é golpe, etc.).
                    - True se não houver indícios suficientes de que a mensagem foi enviada para a pessoa errada.

                    ##Importante: Responda apenas com True ou False, e nada mais.
                    ##Só retorne False quando a resposta do destinatário indicar com clareza que ele(a) não é quem a empresa está tentando contactar ou se ele(a) expressar o desejo de não ##receber mais mensagens, como ao responder "SAIR" (considere erros de digitação).

                    

                    """


def checar_resposta(prompt, telefone, mensagem):

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": prompt},
            {"role": "user", "content": mensagem},
        ],
    )

    return completion.choices[0].message.content


def log_operacao(data_execucao, data_inicial_filtro, registros_alterados):
    log_file = "operacao_log.txt"
    with open(log_file, "a") as f:
        f.write(
            f"Data de Execução: {data_execucao}, Data Inicial do Filtro: {data_inicial_filtro}, Registros Alterados: {registros_alterados}\n"
        )


def classificar_mensagens(data_inicial=hoje):
    try:

        query = f"""
        SELECT 
                    sender_id,
                    STRING_AGG(DISTINCT message_content, ' || ') AS mensagens_concatenadas
                    FROM 
                    message_history
                    Where message_content <> '' and message_content <> 'Resposta automática' and created_at >= '{data_inicial}'
                    GROUP BY 
                    sender_id;
                    """

        # cursor.execute(query)
        query_result = session.execute(text(query))
        query_iterable = query_result.fetchall()

        if query_iterable:
            for resultado in tqdm(
                query_iterable, desc="processando messagens", colour="GREEN"
            ):

                result = checar_resposta(prompt, resultado[0], resultado[1])

                vars = (resultado[0], result, resultado[1])

                session.execute(
                    text(
                        f"""
                            UPDATE contatos SET validado = {result} WHERE telefone LIKE ('%{resultado[0][-8:]}')
                        """
                    )
                )
                session.commit()

            log_operacao(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                data_inicial,
                len(query_iterable),
            )

        else:
            print("Nenhuma mensagem encontrada!")

        session.close()

    except Exception as e:
        session.rollback()

        print(e)
