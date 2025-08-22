# Etapa 1: Imagem base
FROM python:3.9-slim

# Etapa 2: Diretório de trabalho inicial
WORKDIR /api

# Etapa 3: Instalar dependências do sistema (Git e Curl)
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Etapa 4: Clonar o repositório com o código da aplicação
RUN git clone https://github.com/gerlanno/disparador-meta-rtla.git .

# Etapa 5: Instalar as dependências do Python a partir do arquivo clonado
RUN pip3 install --no-cache-dir -r requirements.txt

# Etapa 6: Expor a porta que será usada pela variável de ambiente
EXPOSE 8501

# Etapa 7: Checagem de saúde (Health Check) usando a variável de ambiente
HEALTHCHECK CMD curl --fail http://localhost:${PORT}/_stcore/health || exit 1

# Etapa 8: Comando de inicialização usando a variável de ambiente ${PORT}
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=${PORT}", "--server.address=0.0.0.0"]
