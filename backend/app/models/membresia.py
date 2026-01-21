import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Numeric, Integer, Boolean, JSON

from app.config.database import Base


class Membresia(Base):
    __tablename__ = "membresias"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    nombre = Column(String(50), nullable=False)
    precio_mensual = Column(Numeric(10, 2), nullable=False)

    limite_citas_mes = Column(Integer, nullable=True)
    limite_barberos = Column(Integer, nullable=True)
    tiene_ecommerce = Column(Boolean, default=False)
    tiene_analytics_avanzados = Column(Boolean, default=False)
    tiene_notificaciones_push = Column(Boolean, default=False)
    prioridad_busqueda = Column(Integer, default=0)
    destacado_mapa = Column(Boolean, default=False)

    caracteristicas = Column(JSON, default=dict)
    activo = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
