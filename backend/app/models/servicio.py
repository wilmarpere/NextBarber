import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Numeric, Integer
from sqlalchemy.orm import relationship

from app.config.database import Base


class Servicio(Base):
    __tablename__ = "servicios"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    barberia_id = Column(String(36), ForeignKey("barberias.id"), nullable=False)

    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    categoria = Column(String(50), nullable=True)

    activo = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    barberia = relationship("Barberia", back_populates="servicios")
    citas = relationship("Cita", back_populates="servicio")
