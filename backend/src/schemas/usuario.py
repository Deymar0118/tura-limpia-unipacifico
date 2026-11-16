
import re
from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class PerfilUsuarioCreate(BaseModel):
    """Datos del perfil que se asignará al usuario."""

    documento: str = Field(
        min_length=1,
        max_length=30,
    )
    rol_id: int = Field(gt=0)
    fecha_inicio: date
    estado: bool
    cargo: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    @field_validator("documento")
    @classmethod
    def validar_documento(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("El documento es obligatorio.")

        if not re.fullmatch(r"[A-Za-z0-9.-]+", value):
            raise ValueError(
                "El documento contiene caracteres no permitidos."
            )

        return value

    @field_validator("cargo")
    @classmethod
    def validar_cargo(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value


class UsuarioAdminCreate(BaseModel):
    """Datos para registrar un usuario desde administración."""

    model_config = ConfigDict(extra="forbid")

    nombres: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    nombre_usuario: str = Field(min_length=4, max_length=50)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=72)
    perfil: PerfilUsuarioCreate

    @field_validator("nombres", "apellidos")
    @classmethod
    def validar_nombres(cls, value: str) -> str:
        value = " ".join(value.strip().split())

        caracteres_validos = all(
            caracter.isalpha()
            or caracter.isspace()
            or caracter in "-'’"
            for caracter in value
        )

        if len(value) < 2 or not caracteres_validos:
            raise ValueError(
                "Debe contener entre 2 y 100 caracteres "
                "alfabéticos."
            )

        return value

    @field_validator("nombre_usuario")
    @classmethod
    def validar_nombre_usuario(cls, value: str) -> str:
        value = value.strip()

        if not re.fullmatch(r"[A-Za-z0-9]{4,50}", value):
            raise ValueError(
                "El nombre de usuario debe tener entre 4 y 50 "
                "caracteres alfanuméricos sin espacios."
            )

        return value

    @field_validator("correo")
    @classmethod
    def normalizar_correo(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    @field_validator("password")
    @classmethod
    def validar_password(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError(
                "La contraseña no puede superar 72 bytes."
            )

        return value


class RolUsuarioResponse(BaseModel):
    """Información del rol asignado."""

    id: int
    nombre: str


class PerfilUsuarioResponse(BaseModel):
    """Información del perfil creado."""

    id: UUID
    documento: str
    fecha_inicio: date
    estado: bool
    rol: RolUsuarioResponse


class UsuarioAdminData(BaseModel):
    """Información del usuario registrado."""

    id: UUID
    nombres: str
    apellidos: str
    nombre_usuario: str
    correo: EmailStr
    activo: bool
    perfil: PerfilUsuarioResponse


class UsuarioAdminCreateResponse(BaseModel):
    """Respuesta exitosa del registro administrativo."""

    success: bool = True
    message: str
    data: UsuarioAdminData
