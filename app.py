import sys
import os
import io
from datetime import datetime, timedelta

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__))))
)

import pandas as pd
from pandas import ExcelWriter
from database.db import engine
from utils.logger import Logger
import streamlit as st


st.set_page_config(page_title="Sistema de Disparos", page_icon="📨", layout="wide")

st.image("assets/rtla1.png", width=200)
st.title("Sistema de Disparos")

# FILTROS PADRÕES - CARTORIO - PROTOCOLO - DOCUMENOT - NOME - TELEFONE - DATA DISPARO
# Container de Filtros
container_filtros = st.container(border=True)
container_filtros.subheader("Filtros de Pesquisa")
cartorio_col, protocolo_col, documento_col, nome_col, telefone_col, periodo_disparos = (
    container_filtros.columns(6, gap="small")
)

# Elemento Cartório
with cartorio_col:
    cartorio = st.selectbox(
        "Selecione o Cartório",
        options=[
            cartorio
            for cartorio in pd.read_sql_query("SELECT nome FROM cartorios", con=engine)[
                "nome"
            ].tolist()
        ],
        index=None,
        placeholder="Selecione um cartório",
    )
    if cartorio:
        cartorio_id = int(
            pd.read_sql_query(
                "SELECT id FROM cartorios WHERE nome = %(nome)s",
                con=engine,
                params={"nome": cartorio},
            )["id"].iloc[0]
        )
        print(cartorio_id, type(cartorio_id))
# Elemento Protocolo
with protocolo_col:
    protocolo = st.text_input("Protocolo", placeholder="Digite o protocolo")

# Elemento Documento
with documento_col:
    documento = st.text_input(
        "Digite o CPF",
        placeholder="Digite o documento (Máximo 11 dígitos)",
        max_chars=11,
    )

# Elemento Nome
with nome_col:
    nome = st.text_input("Nome", placeholder="Digite o nome do devedor")

# ELemento Telefone
with telefone_col:
    telefone = st.text_input(
        "Telefone",
        placeholder="Digite o telefone do devedor",
        max_chars=15,
    )

# Elemento Período de Disparos
with periodo_disparos:
    periodo_disparos = st.date_input(
        "Período de Disparos",
        value=[
            pd.to_datetime("today") - pd.Timedelta(days=30),
            pd.to_datetime("today"),
        ],
        format="DD.MM.YYYY",
        help="Selecione o período de disparos",
    )


# Função para converter o df para Excel em memória
def to_excel(df):
    output = io.BytesIO()
    # Usando o XlsxWriter como engine para criar o objeto Excel
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Disparos")
    writer.close()
    processed_data = output.getvalue()

    return processed_data


def get_disparos(
    inicio,
    fim,
    cartorio_id=None,
    protocolo=None,
    documento=None,
    nome=None,
    telefone=None,
):

    query = """
            SELECT 
                t.protocolo,
                d.documento,
                d.nome,
                ze.whatsapp as telefone,            
                TO_CHAR(ze.datainsert, 'DD/MM/YYYY HH24:MI:SS') as data

            FROM zapenviados ze
                LEFT JOIN titulos t ON t.id = ze.titulo_id
            LEFT JOIN devedores d ON d.titulo_id = t.id            
            LEFT JOIN message_history mh ON mh.message_id = ze.messageid              
            WHERE 1=1
            AND mh.message_status = 'sent'          
        """
    params = {}
    if telefone:
        query += " AND ze.whatsapp LIKE %(telefone)s"
        params["telefone"] = f"%{telefone}%"
    if inicio:
        data_inicio = f"{inicio} 00:00:01"
        query += " AND ze.datainsert >= %(inicio)s"
        params["inicio"] = inicio
    if fim:
        data_fim = f"{fim} 23:59:59"
        query += " AND ze.datainsert <= %(fim)s"
        params["fim"] = fim
    if nome:
        query += " AND d.nome ILIKE %(nome)s"
        params["nome"] = f"%{nome}%"
    if protocolo:
        query += " AND t.protocolo = %(protocolo)s"
        params["protocolo"] = protocolo
    if documento:
        query += " AND d.documento = %(documento)s"
        params["documento"] = documento
    if cartorio:
        query += " AND t.cartorio_id = %(cartorio_id)s"
        params["cartorio_id"] = cartorio_id

    query += " AND LENGTH(d.documento) = 11"
    query += " ORDER BY ze.datainsert DESC"

    df = pd.read_sql_query(query, con=engine, params=params)
    if df.empty:
        st.warning("Nenhum disparo encontrado para os filtros selecionados.")
        return None

    return df


if len(periodo_disparos) == 2:
    inicio, fim = periodo_disparos
    inicio_str = inicio.strftime("%Y-%m-%d")
    fim_str = fim.strftime("%Y-%m-%d")

    # Primeiro, apenas obtemos o dataframe
    if cartorio or protocolo or documento or nome or telefone:
        df = get_disparos(
            inicio_str,
            fim_str,
            cartorio_id=cartorio if cartorio else None,
            protocolo=protocolo,
            documento=documento,
            nome=nome,
            telefone=telefone,
        )
    else:
        df = get_disparos(inicio_str, fim_str)

    # Agora, verificamos se o dataframe tem dados para então mostrar tudo
    if not df.empty:
        st.subheader(f"Disparos Encontrados: {len(df)} registros")
        st.dataframe(df, use_container_width=True)

        # --- NOVO TRECHO PARA O BOTÃO DE DOWNLOAD ---

        # 1. Converte o dataframe para um arquivo Excel em memória
        df = df.drop_duplicates()
        df_xlsx = to_excel(df)

        # 2. Cria o botão de download
        st.download_button(
            label="📥 Salvar em Excel (.xlsx)",
            data=df_xlsx,
            file_name=f"relatorio_disparos[{datetime.now()}].xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        # --- FIM DO NOVO TRECHO ---

    else:
        st.info("Nenhum registro encontrado para os filtros selecionados.")

else:
    st.warning("Selecione uma data inicial e uma final.")
