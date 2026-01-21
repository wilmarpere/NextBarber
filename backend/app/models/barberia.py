import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum, ForeignKey, Numeric, Table, JSON
from sqlalchemy.orm import relationship
import enum

from app.config.database import Base


class EstadoBarberia(str, enum.Enum):
    PENDIENTE = "pendiente"
    ACTIVA = "activa"
    SUSPENDIDA = "suspendida"
    CANCELADA = "cancelada"


class PlanMembresia(str, enum.Enum):
    BASICO = "basico"
    PROFESIONAL = "profesional"
    PREMIUM = "premium"


# Tabla intermedia para favoritos
favoritos = Table(
    "favoritos",
    Base.metadata,
    Column("usuario_id", String(36), ForeignKey("usuarios.id"), primary_key=True),
    Column("barberia_id", String(36), ForeignKey("barberias.id"), primary_key=True),
    Column("created_at", DateTime, default=datetime.utcnow)
)


class Barberia(Base):
    __tablename__ = "barberias"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    propietario_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)

    # Información básica
    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    direccion = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)

    # Ubicación geográfica
    latitud = Column(Numeric(10, 8), nullable=True)
    longitud = Column(Numeric(11, 8), nullable=True)

    # Documentos
    nit = Column(String(50), nullable=True)

    # Horarios (JSON: {"lunes": {"apertura": "08:00", "cierre": "20:00"}, ...})
    horario = Column(JSON, nullable=True)

    # Estado y membresía
    estado = Column(Enum(EstadoBarberia), default=EstadoBarberia.PENDIENTE)
    plan_membresia = Column(Enum(PlanMembresia), default=PlanMembresia.BASICO)
    fecha_vencimiento = Column(DateTime, nullable=True)

    # Métricas
    calificacion_promedio = Column(Numeric(2, 1), default=0.0)
    total_resenas = Column(Numeric, default=0)

    # Imágenes
    logo_url = Column(String(500), nullable=True)
    fotos = Column(JSON, default=list)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    propietario = relationship("Usuario", back_populates="barberia")
    servicios = relationship("Servicio", back_populates="barberia", cascade="all, delete-orphan")
    barberos = relationship("Barbero", back_populates="barberia", cascade="all, delete-orphan")
    citas = relationship("Cita", back_populates="barberia", cascade="all, delete-orphan")
    resenas = relationship("Resena", back_populates="barberia", cascade="all, delete-orphan")
    pagos = relationship("Pago", back_populates="barberia", cascade="all, delete-orphan")
    productos = relationship("Producto", back_populates="barberia", cascade="all, delete-orphan")
    favoritos_por = relationship("Usuario", secondary=favoritos, back_populates="favoritos")
