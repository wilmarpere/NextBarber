from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.config.database import get_db
from app.config.settings import settings
from app.models.usuario import Usuario, RolUsuario
from app.schemas.usuario import (
    UsuarioCreate, UsuarioResponse, Token, LoginRequest, CambiarPasswordRequest
)
from app.middlewares.auth import (
    verificar_password, obtener_password_hash,
    crear_access_token, crear_refresh_token, obtener_usuario_actual
)

router = APIRouter()


@router.post("/registro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Solo permitir registro de clientes por esta ruta
    if usuario.rol != RolUsuario.CLIENTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo puedes registrarte como cliente"
        )

    nuevo_usuario = Usuario(
        email=usuario.email,
        password_hash=obtener_password_hash(usuario.password),
        nombre=usuario.nombre,
        telefono=usuario.telefono,
        rol=usuario.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not usuario or not verificar_password(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    access_token = crear_access_token(
        data={"sub": str(usuario.id), "rol": usuario.rol.value}
    )
    refresh_token = crear_refresh_token(
        data={"sub": str(usuario.id)}
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UsuarioResponse)
def obtener_perfil(usuario: Usuario = Depends(obtener_usuario_actual)):
    return usuario


@router.put("/cambiar-password")
def cambiar_password(
    datos: CambiarPasswordRequest,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    if not verificar_password(datos.password_actual, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )

    usuario.password_hash = obtener_password_hash(datos.password_nuevo)
    db.commit()

    return {"message": "Contraseña actualizada correctamente"}
