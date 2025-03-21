from enum import auto
from sqlite3 import Date
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import (
    
    Boolean,
    Numeric,
    Text,
    create_engine,
    Column,
    ForeignKey,
    String,
    Integer,
    CheckConstraint,
    UniqueConstraint,
    TIMESTAMP,
    func,
    PrimaryKeyConstraint,
    null,
    inspect
)
from utils.logger import Logger
from sqlalchemy.orm import sessionmaker, declarative_base
from database.db import create_session, engine

logger = Logger().get_logger()

Base = declarative_base()

class Cartorio(Base):
    __tablename__ = "cartorios"
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    website = Column(String(100))


class Titulo(Base):

    """
    #### Criar o trigger caso precise recriar o banco. ####
    CREATE OR REPLACE FUNCTION set_mesano_insert()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.mesano_insert := TO_CHAR(NEW.datainsert, 'MMYYYY');
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        CREATE TRIGGER trg_set_mesano_insert
        BEFORE INSERT ON titulos
        FOR EACH ROW
        EXECUTE FUNCTION set_mesano_insert();            
    
    """

    __tablename__ = "titulos"

    id = Column(Integer, primary_key=True)
    cartorio_id = Column(Integer, ForeignKey("cartorios.id"))
    protocolo = Column(String(255), nullable=False)  # Removi unique=True
    credor = Column(String, nullable=False)
    valorprotestado = Column(Numeric(10, 2), nullable=False)
    numerotitulo = Column(String(255), nullable=False)
    dataprotesto = Column(String, nullable=False)
    mesano = Column(Integer, nullable=False)
    valorboleto = Column(Numeric(10, 2), nullable=False)
    datainsert = Column(TIMESTAMP, server_default=func.now())

    # Nova coluna para armazenar mês/ano da data de inserção
    mesano_insert = Column(String(6), nullable=False, default=func.to_char(func.now(), 'MMYYYY'))

    # Restrições
    __table_args__ = (
        CheckConstraint("mesano >= 202001 AND mesano <= 210001", name="check_mesano"),
        UniqueConstraint("protocolo", "mesano_insert", name="uq_protocolo_mesano")
    )


class Devedor(Base):
    __tablename__ = "devedores"
    titulo_id = Column(Integer, ForeignKey("titulos.id"), primary_key=True)
    documento = Column(String, nullable=False, primary_key=True)
    nome = Column(String(255), nullable=False)
    PrimaryKeyConstraint("documento", "titulo_id")


class Contato(Base):
    __tablename__ = "contatos"
    documento = Column(String(14), nullable=False, primary_key=True)
    telefone = Column(String(), primary_key=True)
    email = Column(String(100))
    iswhatsapp = Column(Boolean, default=True)  # Nova coluna adicionada com valor padrão
    PrimaryKeyConstraint("documento", "telefone")



class Zapenviado(Base):
    __tablename__ = "zapenviados"

    messageid = Column(String(100))
    titulo_id = Column(Integer, ForeignKey("titulos.id"), primary_key=True)
    whatsapp = Column(String(15), primary_key=True)
    mesano_insert = Column(String(6), nullable=False, primary_key=True)  # Novo campo na chave primária
    wa_id = Column(String(13))
    message_status = Column(String(50))
    accepted = Column(String(255))
    rejected = Column(String(255))
    response = Column(Text)
    error = Column(String(255))
    datainsert = Column(TIMESTAMP, server_default=func.now())



class Template(Base):
    __tablename__ = "templates"
    
    name = Column(String, nullable=False, primary_key=True)
    status = Column(String, nullable=False)
    language = Column(String)
    wbaccount_id = Column(String, ForeignKey(column="wb_accounts.business_account_id"), primary_key=True)
    PrimaryKeyConstraint("name", "wbaccount_id")


class Wb_account(Base):    
    __tablename__ = "wb_accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    phone_id = Column(String, nullable=False, primary_key=True)
    business_account_id = Column(String, nullable=False, unique=True, primary_key=True)
    verified_name = Column(String, nullable=False)
    display_phone_number = Column(String, nullable=False)
    PrimaryKeyConstraint("phone_id", "business_account_id")


def create_tables():
    try:
        Base.metadata.create_all(engine)
        inspector = inspect(engine)
        if "cartorios" in inspector.get_table_names():
            from controller.insrir_cartorios import dados_cartorio
            dados_cartorio()

    except Exception as e:
        logger.error(e)

