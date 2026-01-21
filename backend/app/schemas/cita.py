from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from app.models.cita import EstadoCita


class CitaBase(BaseModel):
    barberia_id: UUID
    servicio_id: UUID
    barbero_id: Optional[UUID] = None
    fecha_hora: datetime
    notas: Optional[str] = None


class CitaCreate(CitaBase):
    pass


class CitaUpdate(BaseModel):
    barbero_id: Optional[UUID] = None
    fecha_hora: Optional[datetime] = None
    estado: Optional[EstadoCita] = None
    notas: Optional[str] = None


class CitaResponse(BaseModel):
    id: UUID
    barberia_id: UUID
    cliente_id: UUID
    servicio_id: UUID
    barbero_id: Optional[UUID] = None
    fecha_hora: datetime
    duracion_minutos: int
    precio_total: Decimal
    estado: EstadoCita
    notas: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
