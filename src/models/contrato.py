from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Contrato(Base):
    """Modelo para representar um contrato público."""
    
    __tablename__ = "contratos"
    
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(100), nullable=False, index=True)
    objeto = Column(Text, nullable=False)
    valor = Column(Float, nullable=False)
    
    # Chave estrangeira para o fornecedor
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=False)
    
    # Relacionamento com fornecedor
    fornecedor = relationship("Fornecedor", back_populates="contratos")
    
    def __repr__(self):
        return f"<Contrato(id={self.id}, numero='{self.numero}', valor={self.valor})>"
