from enum import auto
from sqlite3 import Date
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import (
    
    Numeric,
    Text,
    create_engine,
    Column,
    ForeignKey,
    String,
    Integer,
    CheckConstraint,
    TIMESTAMP,
    func,
    PrimaryKeyConstraint,
    null,
    inspect
)

from sqlalchemy.orm import sessionmaker, declarative_base
from database.db import create_session, engine



Base = declarative_base()

class Cartorio(Base):
    __tablename__ = "cartorios"
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    website = Column(String(100))


class Titulo(Base):
    __tablename__ = "titulos"
    id = Column(Integer, primary_key=True)
    cartorio_id = Column(Integer, ForeignKey("cartorios.id"))
    protocolo = Column(String(255), nullable=False, unique=True)
    credor = Column(String, nullable=False)
    valorprotestado = Column(Numeric(10, 2), nullable=False)
    numerotitulo = Column(String(255), nullable=False)
    dataprotesto = Column(String, nullable=False)
    mesano = Column(Integer, nullable=False)
    CheckConstraint("mesano >= 202001 AND mesano <= 210001", name="check_mesano")
    valorboleto = Column(Numeric(10, 2), nullable=False)
    datainsert = Column(TIMESTAMP, server_default=func.now())


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
    PrimaryKeyConstraint("documento", "telefone")


class Zapenviado(Base):
    __tablename__ = "zapenviados"
    messageid = Column(String(100))
    titulo_id = Column(Integer, ForeignKey("titulos.id"), primary_key=True)
    whatsapp = Column(String(15))
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
        print(e)

