import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.config.database import Base


class Resena(Base):
    __tablename__ = "resenas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    barberia_id = Column(String(36), ForeignKey("barberias.id"), nullable=False)
    cliente_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    cita_id = Column(String(36), ForeignKey("citas.id"), nullable=True)

    calificacion = Column(Integer, nullable=False)
    comentario = Column(Text, nullable=True)
    respuesta_barberia = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    barberia = relationship("Barberia", back_populates="resenas")
    cliente = relationship("Usuario", back_populates="resenas")
