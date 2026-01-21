import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Numeric, Integer, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
import enum

from app.config.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barberia_id = Column(UUID(as_uuid=True), ForeignKey("barberias.id"), nullable=False)

    nombre = Column(String(150), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0)
    categoria = Column(String(50), nullable=True)

    imagen_url = Column(String(500), nullable=True)
    imagenes = Column(JSONB, default=list)

    activo = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    barberia = relationship("Barberia", back_populates="productos")


class EstadoPedido(str, enum.Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    barberia_id = Column(UUID(as_uuid=True), ForeignKey("barberias.id"), nullable=False)
    cliente_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)

    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(Enum(EstadoPedido), default=EstadoPedido.PENDIENTE)

    direccion_envio = Column(Text, nullable=True)
    notas = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    items = relationship("PedidoItem", back_populates="pedido", cascade="all, delete-orphan")


class PedidoItem(Base):
    __tablename__ = "pedido_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pedido_id = Column(UUID(as_uuid=True), ForeignKey("pedidos.id"), nullable=False)
    producto_id = Column(UUID(as_uuid=True), ForeignKey("productos.id"), nullable=False)

    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal = Column(Numeric(10, 2), nullable=False)

    # Relaciones
    pedido = relationship("Pedido", back_populates="items")
