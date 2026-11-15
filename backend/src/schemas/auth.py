from enum import Enum
from pydantic import BaseModel, Field


class RolEnum(str, Enum):
    """Roles del sistema definidos en RF-01."""
    CIUDADANO = "ciudadano"
    TRABAJADOR = "trabajador"
    GERENTE = "gerente"
    ADMIN = "admin"


class LoginRequest(BaseModel):
    """Credenciales de inicio de sesión (RF-06): correo o nombre de usuario y contraseña."""
    # La vista de login envía este dato con el nombre "email"
    identificador: str = Field(..., alias="email", min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    rol: RolEnum


class UsuarioActualResponse(BaseModel):
    """Datos del usuario autenticado que la vista guarda en la sesión."""
    id: str
    nombre: str
    email: str
    rol: RolEnum
