from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from decimal import Decimal
from datetime import datetime

from app.models.pago import MetodoPago, EstadoPago


class PagoBase(BaseModel):
    barberia_id: UUID
    monto: Decimal
    metodo_pago: MetodoPago
    periodo_inicio: datetime
    periodo_fin: datetime
    notas: Optional[str] = None


class PagoCreate(PagoBase):
    pass


class PagoUpdate(BaseModel):
    estado: Optional[EstadoPago] = None
    referencia_externa: Optional[str] = None
    factura_url: Optional[str] = None
    notas: Optional[str] = None


class PagoResponse(PagoBase):
    id: UUID
    estado: EstadoPago
    registrado_por: Optional[UUID] = None
    referencia_externa: Optional[str] = None
    factura_url: Optional[str] = None
    fecha_pago: datetime
    created_at: datetime

    class Config:
        from_attributes = True
