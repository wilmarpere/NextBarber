import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
import enum

from app.config.database import Base


class RolUsuario(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN_BARBERIA = "admin_barberia"
    CLIENTE = "cliente"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=True)
    rol = Column(Enum(RolUsuario), nullable=False, default=RolUsuario.CLIENTE)
    activo = Column(Boolean, default=True)
    avatar_url = Column(String(500), nullable=True)

    # Preferencias
    notificaciones_push = Column(Boolean, default=True)
    notificaciones_whatsapp = Column(Boolean, default=True)
    notificaciones_email = Column(Boolean, default=True)
    modo_oscuro = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    barberia = relationship("Barberia", back_populates="propietario", uselist=False)
    citas = relationship("Cita", back_populates="cliente", foreign_keys="Cita.cliente_id")
    resenas = relationship("Resena", back_populates="cliente")
    favoritos = relationship("Barberia", secondary="favoritos", back_populates="favoritos_por")
