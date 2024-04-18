from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from model import Base
from model.formularioComunidade import FormularioComunidade

class CadastroAssociacao(Base):
    __tablename__ = 'cadastro_associacao'

    cod_assoc = Column(Integer, primary_key=True)
    nome_assoc = Column(String(100), nullable=False, unique=True)
    endereco = Column(String(200), nullable=False, unique=True)
    telefone = Column(String(15), nullable=False, unique=True)
    nome_coord = Column(String(100), nullable=False, unique=True)
    data_cadastro = Column(DateTime, nullable=False, default=func.now())

    formularios = relationship('FormularioComunidade', back_populates='cadastro_assoc', cascade="all, delete-orphan")

    # Lazy import dentro do método
    def add_formulario(self, pergunta, resposta):
        from model.formularioComunidade import FormularioComunidade
        formulario = FormularioComunidade(pergunta=pergunta, resposta=resposta)
        self.formularios.append(formulario)

    def __init__(self, nome_assoc, endereco, telefone, nome_coord, formularios=[]):
            self.nome_assoc = nome_assoc
            self.endereco = endereco
            self.telefone = telefone
            self.nome_coord = nome_coord
            # A data_cadastro será automaticamente definida pelo default=func.now()
            # Adicionando formularios
            for formulario in formularios:
                novo_formulario = FormularioComunidade(
                    pergunta=formulario['pergunta'],
                    resposta=formulario['resposta']
                )
                self.formularios.append(novo_formulario)
                