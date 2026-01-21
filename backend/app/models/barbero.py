import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.config.database import Base


class Barbero(Base):
    __tablename__ = "barberos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barberia_id = Column(UUID(as_uuid=True), ForeignKey("barberias.id"), nullable=False)

    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    foto_url = Column(String(500), nullable=True)
    descripcion = Column(Text, nullable=True)

    # Horarios individuales del barbero
    horario = Column(JSONB, nullable=True)

    activo = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    barberia = relationship("Barberia", back_populates="barberos")
    citas = relationship("Cita", back_populates="barbero")
