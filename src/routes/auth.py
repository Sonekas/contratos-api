from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.models.usuario import Usuario
from src.schemas import Token, UserLogin, UsuarioCreate, Usuario as UsuarioSchema
from src.auth import (
    authenticate_user, 
    create_access_token, 
    get_password_hash, 
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_current_user
)

auth_router = APIRouter()

@auth_router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Endpoint para autenticação de utilizadores."""
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de utilizador ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/register", response_model=UsuarioSchema, status_code=status.HTTP_201_CREATED)
def register(user: UsuarioCreate, db: Session = Depends(get_db)):
    """Endpoint para registo de novos utilizadores."""
    # Verificar se o utilizador já existe
    db_user = db.query(Usuario).filter(Usuario.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de utilizador já registado"
        )
    
    # Criar novo utilizador
    hashed_password = get_password_hash(user.password)
    db_user = Usuario(
        username=user.username,
        hashed_password=hashed_password,
        perfil=user.perfil
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@auth_router.get("/me", response_model=UsuarioSchema)
def read_users_me(current_user: Usuario = Depends(get_current_user)):
    """Obter informações do utilizador atual."""
    return current_user
