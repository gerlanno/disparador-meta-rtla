# --- A Abordagem Final e Simplificada ---
# Este é o método padrão e mais confiável.

FROM python:3.9-slim

# Define um diretório de trabalho limpo
WORKDIR /app

# Instala somente o 'curl', que é necessário para o HEALTHCHECK. Não precisamos mais do git.
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 1. Copia SÓ o arquivo de requisitos primeiro (isso otimiza o cache de forma inteligente)
COPY requirements.txt .

# 2. Instala os pacotes Python
RUN pip3 install streamlit
RUN pip3 install --no-cache-dir -r requirements.txt

# 3. Copia TODO o resto do seu código que o Easypanel já baixou
COPY . .

# Expõe a porta e define a checagem de saúde
EXPOSE 8501
HEALTHCHECK CMD /bin/sh -c 'curl --fail http://localhost:${PORT}/_stcore/health' || exit 1

# Executa o app.py que foi copiado para a raiz do /app
ENTRYPOINT streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0
