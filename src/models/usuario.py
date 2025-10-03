from sqlalchemy import Column, Integer, String
from src.database import Base

class Usuario(Base):
    """Modelo para representar um utilizador do sistema."""
    
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    perfil = Column(String(20), nullable=False, default="leitor")  # "admin" ou "leitor"
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, username='{self.username}', perfil='{self.perfil}')>"
