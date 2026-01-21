import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, Numeric, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.config.database import Base


class Membresia(Base):
    __tablename__ = "membresias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    nombre = Column(String(50), nullable=False)  # basico, profesional, premium
    precio_mensual = Column(Numeric(10, 2), nullable=False)

    # Límites del plan
    limite_citas_mes = Column(Integer, nullable=True)  # null = ilimitadas
    limite_barberos = Column(Integer, nullable=True)   # null = ilimitados
    tiene_ecommerce = Column(Boolean, default=False)
    tiene_analytics_avanzados = Column(Boolean, default=False)
    tiene_notificaciones_push = Column(Boolean, default=False)
    prioridad_busqueda = Column(Integer, default=0)  # 0=normal, 1=media, 2=alta
    destacado_mapa = Column(Boolean, default=False)

    # Características adicionales (JSON para flexibilidad)
    caracteristicas = Column(JSONB, default=dict)

    activo = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
