import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.config.database import Base


class Resena(Base):
    __tablename__ = "resenas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barberia_id = Column(UUID(as_uuid=True), ForeignKey("barberias.id"), nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    cita_id = Column(UUID(as_uuid=True), ForeignKey("citas.id"), nullable=True)

    calificacion = Column(Integer, nullable=False)  # 1-5 estrellas
    comentario = Column(Text, nullable=True)
    respuesta_barberia = Column(Text, nullable=True)  # Respuesta del admin

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    barberia = relationship("Barberia", back_populates="resenas")
    cliente = relationship("Usuario", back_populates="resenas")
