from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.config.database import get_db
from app.models.usuario import Usuario, RolUsuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.middlewares.auth import (
    obtener_usuario_actual, requiere_super_admin, obtener_password_hash
)

router = APIRouter()


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    rol: RolUsuario = None,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Solo Super Admin puede listar todos los usuarios"""
    query = db.query(Usuario)
    if rol:
        query = query.filter(Usuario.rol == rol)
    return query.offset(skip).limit(limit).all()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: UUID,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Solo Super Admin puede ver detalles de cualquier usuario"""
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return db_usuario


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    usuario_data: UsuarioCreate,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin puede crear usuarios con cualquier rol"""
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    nuevo_usuario = Usuario(
        email=usuario_data.email,
        password_hash=obtener_password_hash(usuario_data.password),
        nombre=usuario_data.nombre,
        telefono=usuario_data.telefono,
        rol=usuario_data.rol
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: UUID,
    usuario_data: UsuarioUpdate,
    usuario_actual: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Usuario puede actualizarse a sí mismo o Super Admin a cualquiera"""
    if str(usuario_actual.id) != str(usuario_id) and usuario_actual.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar este usuario"
        )

    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    update_data = usuario_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_usuario, key, value)

    db.commit()
    db.refresh(db_usuario)
    return db_usuario


@router.delete("/{usuario_id}")
def desactivar_usuario(
    usuario_id: UUID,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin puede desactivar usuarios"""
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    db_usuario.activo = False
    db.commit()

    return {"message": "Usuario desactivado correctamente"}
