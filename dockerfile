# Etapa 1: Imagem base
FROM python:3.9-slim

# Etapa 2: Diretório de trabalho
WORKDIR /api

# Etapa 3: Instalar dependências do sistema
# ADICIONADO: libpq-dev e gcc para compilar o psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Etapa 4: Clonar o repositório com o código da aplicação
RUN git clone https://github.com/gerlanno/disparador-meta-rtla.git .

# ADICIONE ESTA LINHA PARA QUEBRAR O CACHE
# Mude o valor sempre que precisar forçar um rebuild
ARG CACHE_BUSTER=2025-08-22-022900

# Etapa 5: Instalar as dependências do Python a partir do arquivo clonado
RUN pip3 install --no-cache-dir -r requirements.txt

# Etapa 6: (OPCIONAL) Verificar se o streamlit foi instalado corretamente
RUN which streamlit

# Etapa 7: Expor a porta e configurar Health Check
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:${PORT}/_stcore/health || exit 1

# Etapa 8: Comando de inicialização
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=${PORT}", "--server.address=0.0.0.0"]
