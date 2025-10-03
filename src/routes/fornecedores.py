from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.fornecedor import Fornecedor
from src.schemas import Fornecedor as FornecedorSchema, FornecedorCreate, FornecedorUpdate
from src.auth import get_current_user, require_admin

fornecedores_router = APIRouter()

@fornecedores_router.get("/", response_model=List[FornecedorSchema])
def listar_fornecedores(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Listar todos os fornecedores."""
    fornecedores = db.query(Fornecedor).offset(skip).limit(limit).all()
    return fornecedores

@fornecedores_router.get("/{fornecedor_id}", response_model=FornecedorSchema)
def obter_fornecedor(
    fornecedor_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obter um fornecedor específico pelo ID."""
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if fornecedor is None:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor

@fornecedores_router.post("/", response_model=FornecedorSchema, status_code=status.HTTP_201_CREATED)
def criar_fornecedor(
    fornecedor: FornecedorCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Criar um novo fornecedor (apenas administradores)."""
    db_fornecedor = Fornecedor(**fornecedor.dict())
    db.add(db_fornecedor)
    db.commit()
    db.refresh(db_fornecedor)
    return db_fornecedor

@fornecedores_router.put("/{fornecedor_id}", response_model=FornecedorSchema)
def atualizar_fornecedor(
    fornecedor_id: int, 
    fornecedor_update: FornecedorUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Atualizar um fornecedor existente (apenas administradores)."""
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if fornecedor is None:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    update_data = fornecedor_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fornecedor, field, value)
    
    db.commit()
    db.refresh(fornecedor)
    return fornecedor

@fornecedores_router.delete("/{fornecedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_fornecedor(
    fornecedor_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Deletar um fornecedor (apenas administradores)."""
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
    if fornecedor is None:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    db.delete(fornecedor)
    db.commit()
    return None
