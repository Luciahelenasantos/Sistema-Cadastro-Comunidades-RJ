from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from model import Base

class FormularioComunidade(Base):
    __tablename__ = 'formulario_comunidade'

    id = Column(Integer, primary_key=True)
    cod_assoc = Column(Integer, ForeignKey('cadastro_associacao.cod_assoc'), nullable=False)
    pergunta = Column(String(300), nullable=False)
    resposta = Column(String(300), nullable=False)
    data_formulario = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    cadastro_assoc = relationship('CadastroAssociacao', back_populates='formularios')

    def __init__(self, cod_assoc, pergunta, resposta):
        self.cod_assoc = cod_assoc
        self.pergunta = pergunta
        self.resposta = resposta
        # A data_formulario será definida pelo default na definição da coluna