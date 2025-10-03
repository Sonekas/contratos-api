import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configuração da base de dados SQLite
DATABASE_URL = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"

# Criar o motor da base de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Criar a sessão da base de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

def get_db():
    """Dependência para obter uma sessão da base de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
