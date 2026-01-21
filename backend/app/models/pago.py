import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.config.database import Base


class MetodoPago(str, enum.Enum):
    TARJETA = "tarjeta"
    TRANSFERENCIA = "transferencia"
    EFECTIVO = "efectivo"
    PSE = "pse"
    NEQUI = "nequi"
    DAVIPLATA = "daviplata"


class EstadoPago(str, enum.Enum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    FALLIDO = "fallido"
    REEMBOLSADO = "reembolsado"


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barberia_id = Column(UUID(as_uuid=True), ForeignKey("barberias.id"), nullable=False)
    registrado_por = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)

    monto = Column(Numeric(10, 2), nullable=False)
    metodo_pago = Column(Enum(MetodoPago), nullable=False)
    estado = Column(Enum(EstadoPago), default=EstadoPago.PENDIENTE)

    # Período de suscripción
    periodo_inicio = Column(DateTime, nullable=False)
    periodo_fin = Column(DateTime, nullable=False)

    # Referencias externas
    referencia_externa = Column(String(255), nullable=True)  # ID de Stripe/ePayco
    factura_url = Column(String(500), nullable=True)

    notas = Column(Text, nullable=True)

    # Timestamps
    fecha_pago = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    barberia = relationship("Barberia", back_populates="pagos")
