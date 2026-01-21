from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime


class ServicioBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    duracion_minutos: int
    categoria: Optional[str] = None


class ServicioCreate(ServicioBase):
    pass


class ServicioUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = None
    duracion_minutos: Optional[int] = None
    categoria: Optional[str] = None
    activo: Optional[bool] = None


class ServicioResponse(ServicioBase):
    id: UUID
    barberia_id: UUID
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True
