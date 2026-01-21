from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime


class ResenaBase(BaseModel):
    calificacion: int = Field(..., ge=1, le=5)
    comentario: Optional[str] = None


class ResenaCreate(ResenaBase):
    barberia_id: UUID
    cita_id: Optional[UUID] = None


class ResenaUpdate(BaseModel):
    calificacion: Optional[int] = Field(None, ge=1, le=5)
    comentario: Optional[str] = None


class ResenaRespuesta(BaseModel):
    respuesta_barberia: str


class ResenaResponse(ResenaBase):
    id: UUID
    barberia_id: UUID
    cliente_id: UUID
    cita_id: Optional[UUID] = None
    respuesta_barberia: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
