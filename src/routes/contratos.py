from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.contrato import Contrato
from src.models.fornecedor import Fornecedor
from src.schemas import Contrato as ContratoSchema, ContratoCreate, ContratoUpdate
from src.auth import get_current_user, require_admin

contratos_router = APIRouter()

@contratos_router.get("/", response_model=List[ContratoSchema])
def listar_contratos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Listar todos os contratos."""
    contratos = db.query(Contrato).offset(skip).limit(limit).all()
    return contratos

@contratos_router.get("/{contrato_id}", response_model=ContratoSchema)
def obter_contrato(
    contrato_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obter um contrato específico pelo ID."""
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if contrato is None:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
    return contrato

@contratos_router.post("/", response_model=ContratoSchema, status_code=status.HTTP_201_CREATED)
def criar_contrato(
    contrato: ContratoCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Criar um novo contrato (apenas administradores)."""
    # Verificar se o fornecedor existe
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == contrato.fornecedor_id).first()
    if not fornecedor:
        raise HTTPException(status_code=400, detail="Fornecedor não encontrado")
    
    db_contrato = Contrato(**contrato.dict())
    db.add(db_contrato)
    db.commit()
    db.refresh(db_contrato)
    return db_contrato

@contratos_router.put("/{contrato_id}", response_model=ContratoSchema)
def atualizar_contrato(
    contrato_id: int, 
    contrato_update: ContratoUpdate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Atualizar um contrato existente (apenas administradores)."""
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if contrato is None:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
    
    update_data = contrato_update.dict(exclude_unset=True)
    
    # Verificar se o fornecedor existe (se fornecedor_id foi fornecido)
    if "fornecedor_id" in update_data:
        fornecedor = db.query(Fornecedor).filter(Fornecedor.id == update_data["fornecedor_id"]).first()
        if not fornecedor:
            raise HTTPException(status_code=400, detail="Fornecedor não encontrado")
    
    for field, value in update_data.items():
        setattr(contrato, field, value)
    
    db.commit()
    db.refresh(contrato)
    return contrato

@contratos_router.delete("/{contrato_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_contrato(
    contrato_id: int, 
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    """Deletar um contrato (apenas administradores)."""
    contrato = db.query(Contrato).filter(Contrato.id == contrato_id).first()
    if contrato is None:
        raise HTTPException(status_code=404, detail="Contrato não encontrado")
    
    db.delete(contrato)
    db.commit()
    return None

@contratos_router.get("/fornecedor/{fornecedor_id}", response_model=List[ContratoSchema])
def listar_contratos_por_fornecedor(
    fornecedor_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Listar contratos de um fornecedor específico."""
    contratos = db.query(Contrato).filter(Contrato.fornecedor_id == fornecedor_id).offset(skip).limit(limit).all()
    return contratos
