import os
import sys
import csv
from sqlalchemy.orm import Session

# Adicionar o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import SessionLocal, engine
from src.models import Fornecedor, Contrato, Usuario
from src.auth import get_password_hash
from src.database import Base

def populate_database():
    """Popular a base de dados com os dados dos ficheiros CSV."""
    
    # Criar as tabelas
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Criar utilizador administrador padrão
        admin_user = db.query(Usuario).filter(Usuario.username == "admin").first()
        if not admin_user:
            admin_user = Usuario(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                perfil="admin"
            )
            db.add(admin_user)
            print("Utilizador administrador criado: admin/admin123")
        
        # Criar utilizador leitor padrão
        reader_user = db.query(Usuario).filter(Usuario.username == "leitor").first()
        if not reader_user:
            reader_user = Usuario(
                username="leitor",
                hashed_password=get_password_hash("leitor123"),
                perfil="leitor"
            )
            db.add(reader_user)
            print("Utilizador leitor criado: leitor/leitor123")
        
        # Popular fornecedores
        fornecedores_file = "/home/ubuntu/data/contratos-2020-csv/dados_normalizados/tabela_empresas.csv"
        if os.path.exists(fornecedores_file):
            with open(fornecedores_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Pular o cabeçalho
                for row in reader:
                    if len(row) >= 2:
                        fornecedor_id = int(row[0].strip('"'))
                        nome = row[1].strip('"')
                        
                        # Verificar se o fornecedor já existe
                        existing = db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()
                        if not existing:
                            fornecedor = Fornecedor(id=fornecedor_id, nome=nome)
                            db.add(fornecedor)
            
            print("Fornecedores populados com sucesso")
        
        # Popular contratos
        contratos_file = "/home/ubuntu/data/contratos-2020-csv/dados_normalizados/tabela_contratos.csv"
        if os.path.exists(contratos_file):
            with open(contratos_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Pular o cabeçalho
                for row in reader:
                    if len(row) >= 7:
                        contrato_id = int(row[0].strip('"'))
                        numero = row[1].strip('"')
                        objeto = row[2].strip('"')
                        valor = float(row[3].strip('"'))
                        fornecedor_id = int(row[6].strip('"'))
                        
                        # Verificar se o contrato já existe
                        existing = db.query(Contrato).filter(Contrato.id == contrato_id).first()
                        if not existing:
                            contrato = Contrato(
                                id=contrato_id,
                                numero=numero,
                                objeto=objeto,
                                valor=valor,
                                fornecedor_id=fornecedor_id
                            )
                            db.add(contrato)
            
            print("Contratos populados com sucesso")
        
        db.commit()
        print("Base de dados populada com sucesso!")
        
    except Exception as e:
        print(f"Erro ao popular a base de dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    populate_database()
