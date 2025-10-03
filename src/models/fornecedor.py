from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class Fornecedor(Base):
    """Modelo para representar um fornecedor/empresa contratada."""
    
    __tablename__ = "fornecedores"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False, index=True)
    
    # Relacionamento com contratos (um fornecedor pode ter vários contratos)
    contratos = relationship("Contrato", back_populates="fornecedor")
    
    def __repr__(self):
        return f"<Fornecedor(id={self.id}, nome='{self.nome}')>"
