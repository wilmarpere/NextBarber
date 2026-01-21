from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.config.database import get_db
from app.models.usuario import Usuario, RolUsuario
from app.models.resena import Resena
from app.models.barberia import Barberia
from app.schemas.resena import ResenaCreate, ResenaUpdate, ResenaResponse, ResenaRespuesta
from app.middlewares.auth import obtener_usuario_actual, requiere_admin_barberia

router = APIRouter()


@router.get("/barberia/{barberia_id}", response_model=List[ResenaResponse])
def listar_resenas(barberia_id: UUID, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """Lista reseñas de una barbería"""
    return db.query(Resena).filter(
        Resena.barberia_id == barberia_id
    ).order_by(Resena.created_at.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=ResenaResponse, status_code=status.HTTP_201_CREATED)
def crear_resena(
    resena_data: ResenaCreate,
    usuario: Usuario = Depends(obtener_usuario_actual),
    db: Session = Depends(get_db)
):
    """Cliente crea una reseña"""
    # Verificar que no haya reseñado ya esta barbería
    existente = db.query(Resena).filter(
        Resena.barberia_id == resena_data.barberia_id,
        Resena.cliente_id == usuario.id
    ).first()

    if existente:
        raise HTTPException(status_code=400, detail="Ya has reseñado esta barbería")

    nueva_resena = Resena(
        barberia_id=resena_data.barberia_id,
        cliente_id=usuario.id,
        cita_id=resena_data.cita_id,
        calificacion=resena_data.calificacion,
        comentario=resena_data.comentario
    )
    db.add(nueva_resena)

    # Actualizar calificación promedio de la barbería
    barberia = db.query(Barberia).filter(Barberia.id == resena_data.barberia_id).first()
    if barberia:
        total = barberia.total_resenas + 1
        promedio_actual = float(barberia.calificacion_promedio or 0)
        nuevo_promedio = ((promedio_actual * (total - 1)) + resena_data.calificacion) / total
        barberia.calificacion_promedio = round(nuevo_promedio, 1)
        barberia.total_resenas = total

    db.commit()
    db.refresh(nueva_resena)
    return nueva_resena


@router.post("/{resena_id}/responder", response_model=ResenaResponse)
def responder_resena(
    resena_id: UUID,
    respuesta: ResenaRespuesta,
    usuario: Usuario = Depends(requiere_admin_barberia),
    db: Session = Depends(get_db)
):
    """Admin de barbería responde a una reseña"""
    resena = db.query(Resena).filter(Resena.id == resena_id).first()
    if not resena:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")

    barberia = db.query(Barberia).filter(Barberia.id == resena.barberia_id).first()
    if str(barberia.propietario_id) != str(usuario.id) and usuario.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    resena.respuesta_barberia = respuesta.respuesta_barberia
    db.commit()
    db.refresh(resena)
    return resena
