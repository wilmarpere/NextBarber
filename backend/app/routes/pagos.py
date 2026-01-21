from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from datetime import datetime, timedelta

from app.config.database import get_db
from app.models.usuario import Usuario, RolUsuario
from app.models.pago import Pago, EstadoPago
from app.models.barberia import Barberia, EstadoBarberia
from app.schemas.pago import PagoCreate, PagoUpdate, PagoResponse
from app.middlewares.auth import requiere_super_admin, requiere_admin_barberia

router = APIRouter()


@router.get("/barberia/{barberia_id}", response_model=List[PagoResponse])
def listar_pagos_barberia(
    barberia_id: UUID,
    usuario: Usuario = Depends(requiere_admin_barberia),
    db: Session = Depends(get_db)
):
    """Lista pagos de una barbería"""
    barberia = db.query(Barberia).filter(Barberia.id == barberia_id).first()
    if not barberia:
        raise HTTPException(status_code=404, detail="Barbería no encontrada")

    if str(barberia.propietario_id) != str(usuario.id) and usuario.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    return db.query(Pago).filter(Pago.barberia_id == barberia_id).order_by(Pago.fecha_pago.desc()).all()


@router.get("/", response_model=List[PagoResponse])
def listar_todos_pagos(
    estado: EstadoPago = None,
    skip: int = 0,
    limit: int = 100,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin: lista todos los pagos"""
    query = db.query(Pago)
    if estado:
        query = query.filter(Pago.estado == estado)
    return query.order_by(Pago.fecha_pago.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=PagoResponse, status_code=status.HTTP_201_CREATED)
def registrar_pago(
    pago_data: PagoCreate,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin: registra un pago manual"""
    barberia = db.query(Barberia).filter(Barberia.id == pago_data.barberia_id).first()
    if not barberia:
        raise HTTPException(status_code=404, detail="Barbería no encontrada")

    nuevo_pago = Pago(
        barberia_id=pago_data.barberia_id,
        registrado_por=usuario.id,
        monto=pago_data.monto,
        metodo_pago=pago_data.metodo_pago,
        periodo_inicio=pago_data.periodo_inicio,
        periodo_fin=pago_data.periodo_fin,
        notas=pago_data.notas,
        estado=EstadoPago.COMPLETADO
    )
    db.add(nuevo_pago)

    # Actualizar fecha de vencimiento de la barbería
    barberia.fecha_vencimiento = pago_data.periodo_fin
    if barberia.estado == EstadoBarberia.SUSPENDIDA:
        barberia.estado = EstadoBarberia.ACTIVA

    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago


@router.put("/{pago_id}", response_model=PagoResponse)
def actualizar_pago(
    pago_id: UUID,
    pago_data: PagoUpdate,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin: actualiza un pago"""
    pago = db.query(Pago).filter(Pago.id == pago_id).first()
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    update_data = pago_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(pago, key, value)

    db.commit()
    db.refresh(pago)
    return pago
