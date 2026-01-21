from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from decimal import Decimal

from app.config.database import get_db
from app.models.usuario import Usuario, RolUsuario
from app.models.barberia import Barberia, EstadoBarberia, PlanMembresia
from app.schemas.barberia import (
    BarberiaCreate, BarberiaUpdate, BarberiaUpdateAdmin,
    BarberiaResponse, BarberiaListResponse
)
from app.middlewares.auth import (
    obtener_usuario_actual, requiere_super_admin, requiere_admin_barberia
)

router = APIRouter()


@router.get("/", response_model=List[BarberiaListResponse])
def listar_barberias(
    skip: int = 0,
    limit: int = 100,
    estado: EstadoBarberia = None,
    plan: PlanMembresia = None,
    lat: Optional[Decimal] = Query(None, description="Latitud del usuario"),
    lng: Optional[Decimal] = Query(None, description="Longitud del usuario"),
    radio_km: Optional[float] = Query(10, description="Radio de búsqueda en km"),
    db: Session = Depends(get_db)
):
    """Lista barberías públicas (solo activas para usuarios no admin)"""
    query = db.query(Barberia)

    # Por defecto solo mostrar activas
    if estado:
        query = query.filter(Barberia.estado == estado)
    else:
        query = query.filter(Barberia.estado == EstadoBarberia.ACTIVA)

    if plan:
        query = query.filter(Barberia.plan_membresia == plan)

    # Ordenar por prioridad de plan (premium primero)
    query = query.order_by(Barberia.plan_membresia.desc(), Barberia.calificacion_promedio.desc())

    return query.offset(skip).limit(limit).all()


@router.get("/admin", response_model=List[BarberiaResponse])
def listar_todas_barberias(
    skip: int = 0,
    limit: int = 100,
    estado: EstadoBarberia = None,
    plan: PlanMembresia = None,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin: lista todas las barberías con todos los estados"""
    query = db.query(Barberia)

    if estado:
        query = query.filter(Barberia.estado == estado)
    if plan:
        query = query.filter(Barberia.plan_membresia == plan)

    return query.offset(skip).limit(limit).all()


@router.get("/{barberia_id}", response_model=BarberiaResponse)
def obtener_barberia(barberia_id: UUID, db: Session = Depends(get_db)):
    """Obtener detalle de una barbería"""
    barberia = db.query(Barberia).filter(Barberia.id == barberia_id).first()
    if not barberia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada"
        )
    return barberia


@router.post("/", response_model=BarberiaResponse, status_code=status.HTTP_201_CREATED)
def crear_barberia(
    barberia_data: BarberiaCreate,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin: crea una nueva barbería"""
    nueva_barberia = Barberia(
        propietario_id=usuario.id,  # Se asignará al admin de barbería después
        nombre=barberia_data.nombre,
        descripcion=barberia_data.descripcion,
        direccion=barberia_data.direccion,
        telefono=barberia_data.telefono,
        email=barberia_data.email,
        nit=barberia_data.nit,
        latitud=barberia_data.latitud,
        longitud=barberia_data.longitud,
        horario=barberia_data.horario,
        plan_membresia=barberia_data.plan_membresia,
        estado=EstadoBarberia.PENDIENTE
    )
    db.add(nueva_barberia)
    db.commit()
    db.refresh(nueva_barberia)
    return nueva_barberia


@router.put("/{barberia_id}", response_model=BarberiaResponse)
def actualizar_barberia(
    barberia_id: UUID,
    barberia_data: BarberiaUpdate,
    usuario: Usuario = Depends(requiere_admin_barberia),
    db: Session = Depends(get_db)
):
    """Admin de barbería puede actualizar su barbería"""
    barberia = db.query(Barberia).filter(Barberia.id == barberia_id).first()
    if not barberia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada"
        )

    # Verificar que sea el propietario o super admin
    if str(barberia.propietario_id) != str(usuario.id) and usuario.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para editar esta barbería"
        )

    update_data = barberia_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(barberia, key, value)

    db.commit()
    db.refresh(barberia)
    return barberia


@router.put("/{barberia_id}/admin", response_model=BarberiaResponse)
def actualizar_barberia_admin(
    barberia_id: UUID,
    barberia_data: BarberiaUpdateAdmin,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin: puede actualizar ubicación, estado y plan"""
    barberia = db.query(Barberia).filter(Barberia.id == barberia_id).first()
    if not barberia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada"
        )

    update_data = barberia_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(barberia, key, value)

    db.commit()
    db.refresh(barberia)
    return barberia


@router.post("/{barberia_id}/activar", response_model=BarberiaResponse)
def activar_barberia(
    barberia_id: UUID,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin: activa una barbería"""
    barberia = db.query(Barberia).filter(Barberia.id == barberia_id).first()
    if not barberia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada"
        )

    barberia.estado = EstadoBarberia.ACTIVA
    db.commit()
    db.refresh(barberia)
    return barberia


@router.post("/{barberia_id}/suspender", response_model=BarberiaResponse)
def suspender_barberia(
    barberia_id: UUID,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin: suspende una barbería"""
    barberia = db.query(Barberia).filter(Barberia.id == barberia_id).first()
    if not barberia:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Barbería no encontrada"
        )

    barberia.estado = EstadoBarberia.SUSPENDIDA
    db.commit()
    db.refresh(barberia)
    return barberia
