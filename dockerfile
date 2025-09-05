# --- Dockerfile Definitivo ---
# COPIE E COLE TODO ESTE CONTEÚDO

FROM python:3.9-slim

WORKDIR /

RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# --- LINHA CRÍTICA PARA QUEBRAR O CACHE ---
# Altere este valor para a data/hora atual antes de cada deploy para forçar a atualização
ARG CACHE_BUSTER=2025-09-210200

# Lembre-se de usar psycopg2-binary no seu requirements.txt
RUN pip3 install streamlit
RUN pip3 install --no-cache-dir -r requirements.txt

# Etapa 6: Copia TODO o resto do seu código para dentro da imagem
COPY . .

EXPOSE 8501

HEALTHCHECK CMD /bin/sh -c 'curl --fail http://localhost:${PORT}/_stcore/health' || exit 1

# Comando final apontando para o app.py na raiz
ENTRYPOINT streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0
