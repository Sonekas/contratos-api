import os
import sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Adicionar o diretório pai ao path para importações
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.database import engine, Base
from src.routes.auth import auth_router
from src.routes.fornecedores import fornecedores_router
from src.routes.contratos import contratos_router

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Contratos Públicos",
    description="API RESTful para gestão de contratos públicos utilizando dados do portal dados.gov.br",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth_router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(fornecedores_router, prefix="/api/fornecedores", tags=["Fornecedores"])
app.include_router(contratos_router, prefix="/api/contratos", tags=["Contratos"])

# Servir arquivos estáticos
static_folder = os.path.join(os.path.dirname(__file__), 'static')
if os.path.exists(static_folder):
    app.mount("/static", StaticFiles(directory=static_folder), name="static")

@app.get("/")
async def serve_frontend():
    """Servir a página principal da aplicação."""
    index_path = os.path.join(static_folder, 'index.html')
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "API de Contratos Públicos", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
