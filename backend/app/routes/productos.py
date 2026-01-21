from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.config.database import get_db
from app.models.usuario import Usuario, RolUsuario
from app.models.producto import Producto
from app.models.barberia import Barberia, PlanMembresia
from app.middlewares.auth import obtener_usuario_actual, requiere_admin_barberia

router = APIRouter()


@router.get("/barberia/{barberia_id}")
def listar_productos(barberia_id: UUID, activos: bool = True, db: Session = Depends(get_db)):
    """Lista productos de una barbería"""
    query = db.query(Producto).filter(Producto.barberia_id == barberia_id)
    if activos:
        query = query.filter(Producto.activo == True)
    return query.all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_producto(
    barberia_id: UUID,
    nombre: str,
    precio: float,
    descripcion: str = None,
    stock: int = 0,
    categoria: str = None,
    imagen_url: str = None,
    usuario: Usuario = Depends(requiere_admin_barberia),
    db: Session = Depends(get_db)
):
    """Admin de barbería crea un producto (requiere plan Profesional o Premium)"""
    barberia = db.query(Barberia).filter(Barberia.id == barberia_id).first()
    if not barberia:
        raise HTTPException(status_code=404, detail="Barbería no encontrada")

    if str(barberia.propietario_id) != str(usuario.id) and usuario.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    # Verificar plan de membresía
    if barberia.plan_membresia == PlanMembresia.BASICO:
        raise HTTPException(
            status_code=403,
            detail="El e-commerce de productos requiere plan Profesional o Premium"
        )

    nuevo_producto = Producto(
        barberia_id=barberia_id,
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock,
        categoria=categoria,
        imagen_url=imagen_url
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


@router.put("/{producto_id}")
def actualizar_producto(
    producto_id: UUID,
    nombre: str = None,
    descripcion: str = None,
    precio: float = None,
    stock: int = None,
    categoria: str = None,
    imagen_url: str = None,
    activo: bool = None,
    usuario: Usuario = Depends(requiere_admin_barberia),
    db: Session = Depends(get_db)
):
    """Actualizar producto"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    barberia = db.query(Barberia).filter(Barberia.id == producto.barberia_id).first()
    if str(barberia.propietario_id) != str(usuario.id) and usuario.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    if nombre is not None:
        producto.nombre = nombre
    if descripcion is not None:
        producto.descripcion = descripcion
    if precio is not None:
        producto.precio = precio
    if stock is not None:
        producto.stock = stock
    if categoria is not None:
        producto.categoria = categoria
    if imagen_url is not None:
        producto.imagen_url = imagen_url
    if activo is not None:
        producto.activo = activo

    db.commit()
    db.refresh(producto)
    return producto


@router.delete("/{producto_id}")
def eliminar_producto(
    producto_id: UUID,
    usuario: Usuario = Depends(requiere_admin_barberia),
    db: Session = Depends(get_db)
):
    """Desactivar producto"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    barberia = db.query(Barberia).filter(Barberia.id == producto.barberia_id).first()
    if str(barberia.propietario_id) != str(usuario.id) and usuario.rol != RolUsuario.SUPER_ADMIN:
        raise HTTPException(status_code=403, detail="No tienes permisos")

    producto.activo = False
    db.commit()
    return {"message": "Producto eliminado"}
