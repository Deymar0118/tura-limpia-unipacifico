
from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class RolEnum(str, Enum):
    """Roles del sistema definidos en RF-01."""

    CIUDADANO = "ciudadano"
    TRABAJADOR = "trabajador"
    GERENTE = "gerente"
    ADMIN = "admin"


class RegistroRequest(BaseModel):
    """Datos necesarios para registrar un ciudadano."""

    nombres: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    nombre_usuario: str = Field(min_length=3, max_length=50)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=72)
    telefono: str | None = Field(default=None, max_length=20)

    @field_validator("nombres", "apellidos", "nombre_usuario")
    @classmethod
    def limpiar_texto(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("Este campo no puede estar vacío.")
        return valor

    @field_validator("correo")
    @classmethod
    def normalizar_correo(cls, valor: EmailStr) -> str:
        return str(valor).strip().lower()

    @field_validator("nombre_usuario")
    @classmethod
    def normalizar_usuario(cls, valor: str) -> str:
        return valor.strip().lower()

    @field_validator("password")
    @classmethod
    def validar_longitud_password(cls, valor: str) -> str:
        if len(valor.encode("utf-8")) > 72:
            raise ValueError(
                "La contraseña no puede superar los 72 bytes."
            )
        return valor


class RegistroResponse(BaseModel):
    """Respuesta después de registrar un ciudadano."""

    id: str
    nombre: str
    email: str
    rol: RolEnum
    mensaje: str


class LoginRequest(BaseModel):
    """Credenciales para iniciar sesión."""

    model_config = ConfigDict(populate_by_name=True)

    identificador: str = Field(
        ...,
        alias="email",
        min_length=1,
        max_length=100,
        description="Correo electrónico o nombre de usuario.",
        examples=["admin@turalimpia.com"],
    )

    password: str = Field(
        ...,
        min_length=1,
        max_length=128,
        description="Contraseña del usuario.",
    )


class TokenResponse(BaseModel):
    """Respuesta de autenticación."""

    access_token: str = Field(
        ...,
        description="JWT de acceso.",
    )

    token_type: str = Field(
        default="bearer",
        description="Tipo de token.",
    )


class TokenPayload(BaseModel):
    """Información contenida en el JWT."""

    sub: str
    rol: RolEnum


class UsuarioActualResponse(BaseModel):
    """Información del usuario autenticado."""

    id: str
    nombre: str
    email: str
    rol: RolEnum
