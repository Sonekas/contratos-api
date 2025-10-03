from pydantic import BaseModel
from typing import List, Optional

# Schemas para Fornecedor
class FornecedorBase(BaseModel):
    nome: str

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorUpdate(BaseModel):
    nome: Optional[str] = None

class Fornecedor(FornecedorBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para Contrato
class ContratoBase(BaseModel):
    numero: str
    objeto: str
    valor: float
    fornecedor_id: int

class ContratoCreate(ContratoBase):
    pass

class ContratoUpdate(BaseModel):
    numero: Optional[str] = None
    objeto: Optional[str] = None
    valor: Optional[float] = None
    fornecedor_id: Optional[int] = None

class Contrato(ContratoBase):
    id: int
    fornecedor: Optional[Fornecedor] = None
    
    class Config:
        from_attributes = True

# Schemas para Usuario
class UsuarioBase(BaseModel):
    username: str
    perfil: str = "leitor"

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    perfil: Optional[str] = None
    password: Optional[str] = None

class Usuario(UsuarioBase):
    id: int
    
    class Config:
        from_attributes = True

# Schemas para autenticação
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
