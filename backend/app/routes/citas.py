from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime

from app.config.database import get_db
from app.models.usuario import Usuario, RolUsuario
from app.models.cita import Cita, EstadoCita
from app.models.servicio import Servicio
from app.models.barberia import Barberia
from app.schemas.cita import CitaCreate, CitaUpdate, CitaResponse
from app.middlewares.auth import obtener_usuario_actual, requiere_admin_barberia

router = APIRouter()


@router.get("/mis-citas", response_model=List[CitaResponse])
def mis_citas(
    estado: EstadoCita = None,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Cliente: obtiene sus citas"""
    query = db.query(Cita).filter(Cita.cliente_id == usuario.id)
    if estado:
        query = query.filter(Cita.estado == estado)
    return query.order_by(Cita.fecha_hora.desc()).all()


@router.get("/barberia/{barberia_id}", response_model=List[CitaResponse])
def citas_barberia(
    barberia_id: UUID,
    fecha_inicio: datetime = None,
    fecha_fin: datetime = None,
    estado: EstadoCita = None,
    usuario: Usuario = Depends(requiere_admin_barberia),
    db: Session = Depends(get_db)
):
    """Admin barbería: obtiene citas de su barbería"""
    barberia = db.query(Barberia).filter(Barberia.id == barberia_id).first()
    if not barberia:
        raise HTTPException(status_code=404, detail="Barbería no encontrada")

    if str(barberia.propietario_id) != str(usuario.id) and usuario.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    query = db.query(Cita).filter(Cita.barberia_id == barberia_id)

    if fecha_inicio:
        query = query.filter(Cita.fecha_hora >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Cita.fecha_hora <= fecha_fin)
    if estado:
        query = query.filter(Cita.estado == estado)

    return query.order_by(Cita.fecha_hora).all()


@router.post("/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(
    cita_data: CitaCreate,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Cliente: reserva una cita"""
    servicio = db.query(Servicio).filter(Servicio.id == cita_data.servicio_id).first()
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")

    nueva_cita = Cita(
        barberia_id=cita_data.barberia_id,
        cliente_id=usuario.id,
        servicio_id=cita_data.servicio_id,
        barbero_id=cita_data.barbero_id,
        fecha_hora=cita_data.fecha_hora,
        duracion_minutos=servicio.duracion_minutos,
        precio_total=servicio.precio,
        notas=cita_data.notas,
        estado=EstadoCita.PENDIENTE
    )
    db.add(nueva_cita)
    db.commit()
    db.refresh(nueva_cita)
    return nueva_cita


@router.put("/{cita_id}", response_model=CitaResponse)
def actualizar_cita(
    cita_id: UUID,
    cita_data: CitaUpdate,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Actualizar estado de cita"""
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    # Verificar permisos
    barberia = db.query(Barberia).filter(Barberia.id == cita.barberia_id).first()
    es_cliente = str(cita.cliente_id) == str(usuario.id)
    es_admin = str(barberia.propietario_id) == str(usuario.id) or usuario.rol == RolUsuario.SUPER_ADMIN

    if not es_cliente and not es_admin:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    update_data = cita_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(cita, key, value)

    db.commit()
    db.refresh(cita)
    return cita


@router.post("/{cita_id}/cancelar", response_model=CitaResponse)
def cancelar_cita(
    cita_id: UUID,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Cancelar una cita"""
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    if str(cita.cliente_id) != str(usuario.id) and usuario.rol not in [RolUsuario.SUPER_ADMIN, RolUsuario.ADMIN_BARBERIA]:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    cita.estado = EstadoCita.CANCELADA
    db.commit()
    db.refresh(cita)
    return cita
