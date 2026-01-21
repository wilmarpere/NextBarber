from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID
from decimal import Decimal

from app.models.barberia import EstadoBarberia, PlanMembresia


class BarberiaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    direccion: str
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    nit: Optional[str] = None


class BarberiaCreate(BarberiaBase):
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    plan_membresia: PlanMembresia = PlanMembresia.BASICO
    horario: Optional[Dict[str, Any]] = None


class BarberiaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    horario: Optional[Dict[str, Any]] = None
    logo_url: Optional[str] = None
    fotos: Optional[List[str]] = None


class BarberiaUpdateAdmin(BarberiaUpdate):
    """Solo Super Admin puede modificar estos campos"""
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    estado: Optional[EstadoBarberia] = None
    plan_membresia: Optional[PlanMembresia] = None
    fecha_vencimiento: Optional[datetime] = None


class BarberiaResponse(BarberiaBase):
    id: UUID
    propietario_id: UUID
    estado: EstadoBarberia
    plan_membresia: PlanMembresia
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    horario: Optional[Dict[str, Any]] = None
    calificacion_promedio: Decimal
    total_resenas: int
    logo_url: Optional[str] = None
    fotos: List[str] = []
    fecha_vencimiento: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BarberiaListResponse(BaseModel):
    id: UUID
    nombre: str
    direccion: str
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    calificacion_promedio: Decimal
    logo_url: Optional[str] = None
    estado: EstadoBarberia
    plan_membresia: PlanMembresia

    class Config:
        from_attributes = True
