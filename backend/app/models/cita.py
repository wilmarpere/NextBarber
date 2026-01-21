import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum

from app.config.database import Base


class EstadoCita(str, enum.Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    EN_PROGRESO = "en_progreso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"
    NO_ASISTIO = "no_asistio"


class Cita(Base):
    __tablename__ = "citas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barberia_id = Column(UUID(as_uuid=True), ForeignKey("barberias.id"), nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    barbero_id = Column(UUID(as_uuid=True), ForeignKey("barberos.id"), nullable=True)
    servicio_id = Column(UUID(as_uuid=True), ForeignKey("servicios.id"), nullable=False)

    fecha_hora = Column(DateTime, nullable=False)
    duracion_minutos = Column(Numeric, nullable=False)
    precio_total = Column(Numeric(10, 2), nullable=False)

    estado = Column(Enum(EstadoCita), default=EstadoCita.PENDIENTE)
    notas = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    barberia = relationship("Barberia", back_populates="citas")
    cliente = relationship("Usuario", back_populates="citas", foreign_keys=[cliente_id])
    barbero = relationship("Barbero", back_populates="citas")
    servicio = relationship("Servicio", back_populates="citas")
