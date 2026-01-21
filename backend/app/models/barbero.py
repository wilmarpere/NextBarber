import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.config.database import Base


class Barbero(Base):
    __tablename__ = "barberos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    barberia_id = Column(String(36), ForeignKey("barberias.id"), nullable=False)

    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    foto_url = Column(String(500), nullable=True)
    descripcion = Column(Text, nullable=True)

    horario = Column(JSON, nullable=True)
    activo = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    barberia = relationship("Barberia", back_populates="barberos")
    citas = relationship("Cita", back_populates="barbero")
