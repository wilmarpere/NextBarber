from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.config.database import get_db
from app.models.usuario import Usuario, RolUsuario
from app.models.servicio import Servicio
from app.models.barberia import Barberia
from app.schemas.servicio import ServicioCreate, ServicioUpdate, ServicioResponse
from app.middlewares.auth import obtener_usuario_actual, requiere_admin_barberia

router = APIRouter()


@router.get("/barberia/{barberia_id}", response_model=List[ServicioResponse])
def listar_servicios(barberia_id: UUID, activos: bool = True, db: Session = Depends(get_db)):
    """Lista servicios de una barbería"""
    query = db.query(Servicio).filter(Servicio.barberia_id == barberia_id)
    if activos:
        query = query.filter(Servicio.activo == True)
    return query.all()


@router.post("/", response_model=ServicioResponse, status_code=status.HTTP_201_CREATED)
def crear_servicio(
    servicio_data: ServicioCreate,
    barberia_id: UUID,
    usuario: Usuario = Depends(requiere_admin_barberia),
    db: Session = Depends(get_db)
):
    """Admin de barbería crea un servicio"""
    barberia = db.query(Barberia).filter(Barberia.id == barberia_id).first()
    if not barberia:
        raise HTTPException(status_code=404, detail="Barbería no encontrada")

    if str(barberia.propietario_id) != str(usuario.id) and usuario.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    nuevo_servicio = Servicio(barberia_id=barberia_id, **servicio_data.model_dump())
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio


@router.put("/{servicio_id}", response_model=ServicioResponse)
def actualizar_servicio(
    servicio_id: UUID,
    servicio_data: ServicioUpdate,
    usuario: Usuario = Depends(requiere_admin_barberia),
    db: Session = Depends(get_db)
):
    """Actualizar un servicio"""
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    barberia = db.query(Barberia).filter(Barberia.id == servicio.barberia_id).first()
    if str(barberia.propietario_id) != str(usuario.id) and usuario.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    update_data = servicio_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(servicio, key, value)

    db.commit()
    db.refresh(servicio)
    return servicio


@router.delete("/{servicio_id}")
def eliminar_servicio(
    servicio_id: UUID,
    usuario: Usuario = Depends(requiere_admin_barberia),
    db: Session = Depends(get_db)
):
    """Desactivar un servicio"""
    servicio = db.query(Servicio).filter(Servicio.id == servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    barberia = db.query(Barberia).filter(Barberia.id == servicio.barberia_id).first()
    if str(barberia.propietario_id) != str(usuario.id) and usuario.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    servicio.activo = False
    db.commit()
    return {"message": "Servicio eliminado"}
