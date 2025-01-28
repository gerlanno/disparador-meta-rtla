from sqlite3 import connect
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
from config.configs import db_config
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from psycopg2 import sql
from utils.logger import Logger

logger = Logger().get_logger()

HOST = db_config.get("host")
PORT = db_config.get("port")
DATABASE = db_config.get("database")
USER = db_config.get("user")
PASSWORD = db_config.get("password")



admin_engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/postgres")

# Conexão com o banco de administração padrão 'postgres'


def create_database_if_not_exists():
    try:
        # Conecta usando psycopg2 para executar comandos SQL diretamente
            conn = psycopg2.connect(
            dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT
        ) 
            # Necessário para criar o banco de dados
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            conn.autocommit = True
            cursor = conn.cursor()
            # Verifica se o banco de dados existe
            cursor.execute(
                sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"),
                [DATABASE],
            )
            exists = cursor.fetchone()
            if not exists:
                # Cria o banco de dados se não existir
                cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE)))
                print(f"Banco de dados '{DATABASE}' criado com sucesso.")
                return True
            else:
                
                #print(f"Banco de dados '{DATABASE}' já existe.")
                return False

            cursor.close()
            conn.close()

    except Exception as e:
        logger.info(f"Erro ao criar banco de dados: {e}")        
        return False
    
    return True
# Chama a função


# Agora você pode conectar usando o SQLAlchemy
CONNECTION = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(CONNECTION, echo=True)

def check_tables():

    tables_created = inspect(engine).get_table_names()

    return tables_created

def create_session():
 
    Session = sessionmaker(bind=engine)    
    
    return Session()
