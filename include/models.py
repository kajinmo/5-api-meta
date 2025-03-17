# modelo: representação do banco de dados
# view: como os dados vão vir - do request / schema
# não necessariamente o schema tem que ser igual ao model
from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.sql import func
from .db import Base

class Campaign(Base):
    __tablename__ = 'campaign'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # ID único para cada registro
    spend = Column(Float, nullable=False)  # Valor gasto na campanha
    cpc = Column(Float, nullable=False)  # Custo por clique
    cpm = Column(Float, nullable=False)  # Custo por mil impressões
    objective = Column(String, nullable=False)  # Objetivo da campanha (ex: LINK_CLICKS)
    clicks = Column(Integer, nullable=False)  # Número de cliques
    campaign_name = Column(String, nullable=False)  # Nome da campanha
    campaign_id = Column(String, nullable=False)  # ID da campanha
    frequency = Column(Float, nullable=False)  # Frequência de exibição
    date_start = Column(Date, nullable=False)  # Data de início da campanha
    date_stop = Column(Date, nullable=False)  # Data de término da campanha
    created_at = Column(DateTime, default=func.now())  # Data de criação do registro no banco de dados