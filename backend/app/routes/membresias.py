from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.config.database import get_db
from app.models.usuario import Usuario
from app.models.membresia import Membresia
from app.middlewares.auth import requiere_super_admin

router = APIRouter()


@router.get("/", response_model=List[dict])
def listar_membresias(db: Session = Depends(get_db)):
    """Lista planes de membresía disponibles"""
    return db.query(Membresia).filter(Membresia.activo == True).all()


@router.get("/{membresia_id}")
def obtener_membresia(membresia_id: UUID, db: Session = Depends(get_db)):
    """Obtiene detalle de una membresía"""
    membresia = db.query(Membresia).filter(Membresia.id == membresia_id).first()
    if not membresia:
        raise HTTPException(status_code=404, detail="Membresía no encontrada")
    return membresia


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_membresia(
    nombre: str,
    precio_mensual: float,
    limite_citas_mes: int = None,
    limite_barberos: int = None,
    tiene_ecommerce: bool = False,
    tiene_analytics_avanzados: bool = False,
    tiene_notificaciones_push: bool = False,
    prioridad_busqueda: int = 0,
    destacado_mapa: bool = False,
    usuario: Usuario = Depends(requiere_super_admin),
    db: Session = Depends(get_db)
):
    """Super Admin: crea un plan de membresía"""
    nueva_membresia = Membresia(
        nombre=nombre,
        precio_mensual=precio_mensual,
        limite_citas_mes=limite_citas_mes,
        limite_barberos=limite_barberos,
        tiene_ecommerce=tiene_ecommerce,
        tiene_analytics_avanzados=tiene_analytics_avanzados,
        tiene_notificaciones_push=tiene_notificaciones_push,
        prioridad_busqueda=prioridad_busqueda,
        destacado_mapa=destacado_mapa
    )
    db.add(nueva_membresia)
    db.commit()
    db.refresh(nueva_membresia)
    return nueva_membresia
