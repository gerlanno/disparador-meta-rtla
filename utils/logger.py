import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import inspect
import stat

class Logger:
    def __init__(self):
        # Cria o diretório de logs se não existir
        diretorio_atual = os.path.dirname(os.path.realpath(__file__))
        self.diretorio_raiz = os.path.abspath(os.path.join(diretorio_atual, ".."))

        log_directory = os.path.join(self.diretorio_raiz, "logs")
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
            os.chmod(log_directory, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        # Nome do arquivo de log baseado na data de criação
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(log_directory, f"{current_date}.log")

        # Configura o handler para rotação de arquivos
        handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1)
        handler.suffix = "%Y-%m-%d"  # Sufixo de rotação do arquivo

        # Configura o formato do log para incluir o nome do script
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s - Script: %(filename)s"
        )
        handler.setFormatter(formatter)

        # Configura o logger
        self.logger = logging.getLogger(__name__)  # Usamos o logger root para compartilhar entre scripts
        self.logger.setLevel(logging.INFO)

        # Evita múltiplos handlers (verifica se o handler já foi adicionado)
        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

    def get_logger(self):

        # Pega o nome do script chamador
        caller = inspect.stack()[1].filename
        # Logger root já configurado, só retornamos
        return self.logger