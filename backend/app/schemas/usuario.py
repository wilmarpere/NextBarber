from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from uuid import UUID

from app.models.usuario import RolUsuario


class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str
    telefono: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    password: str
    rol: RolUsuario = RolUsuario.CLIENTE


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    avatar_url: Optional[str] = None
    notificaciones_push: Optional[bool] = None
    notificaciones_whatsapp: Optional[bool] = None
    notificaciones_email: Optional[bool] = None
    modo_oscuro: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: UUID
    rol: RolUsuario
    activo: bool
    avatar_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CambiarPasswordRequest(BaseModel):
    password_actual: str
    password_nuevo: str
