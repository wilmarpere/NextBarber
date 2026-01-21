from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.routes import auth, usuarios, barberias, servicios, citas, resenas, membresias, pagos, productos

app = FastAPI(
    title="NextBarber API",
    description="API para la plataforma SaaS de gestión de barberías",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])
app.include_router(usuarios.router, prefix="/api/v1/usuarios", tags=["Usuarios"])
app.include_router(barberias.router, prefix="/api/v1/barberias", tags=["Barberías"])
app.include_router(servicios.router, prefix="/api/v1/servicios", tags=["Servicios"])
app.include_router(citas.router, prefix="/api/v1/citas", tags=["Citas"])
app.include_router(resenas.router, prefix="/api/v1/resenas", tags=["Reseñas"])
app.include_router(membresias.router, prefix="/api/v1/membresias", tags=["Membresías"])
app.include_router(pagos.router, prefix="/api/v1/pagos", tags=["Pagos"])
app.include_router(productos.router, prefix="/api/v1/productos", tags=["Productos"])


@app.get("/")
def root():
    return {"message": "NextBarber API v1.0.0", "docs": "/api/docs"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
