# --- Dockerfile Definitivo ---
# COPIE E COLE TODO ESTE CONTEÚDO

FROM python:3.9-slim

WORKDIR /api

RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# --- LINHA CRÍTICA PARA QUEBRAR O CACHE ---
# Altere este valor para a data/hora atual antes de cada deploy para forçar a atualização
ARG CACHE_BUSTER=2025-08-22-153600

# Esta etapa agora será executada novamente, pegando a versão mais recente do seu código
RUN git clone https://github.com/gerlanno/disparador-meta-rtla.git .

# Lembre-se de usar psycopg2-binary no seu requirements.txt
RUN pip3 install streamlit
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD /bin/sh -c 'curl --fail http://localhost:${PORT}/_stcore/health' || exit 1

# Comando final apontando para o app.py na raiz
ENTRYPOINT streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0
