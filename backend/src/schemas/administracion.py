
from datetime import date, datetime
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from src.schemas.auth import RolEnum


class UsuarioCrearRequest(BaseModel):
    """Datos para crear un usuario desde administración."""

    nombres: str = Field(min_length=2, max_length=100)
    apellidos: str = Field(min_length=2, max_length=100)
    nombre_usuario: str = Field(min_length=3, max_length=50)
    correo: EmailStr
    password: str = Field(min_length=8, max_length=72)
    telefono: str | None = Field(default=None, max_length=20)
    documento: str | None = Field(default=None, max_length=30)
    id_barrio: int | None = None
    rol: RolEnum

    @field_validator("nombres", "apellidos")
    @classmethod
    def limpiar_nombres(cls, valor: str) -> str:
        valor = valor.strip()
        if not valor:
            raise ValueError("Este campo no puede estar vacío.")
        return valor

    @field_validator("nombre_usuario")
    @classmethod
    def normalizar_usuario(cls, valor: str) -> str:
        valor = valor.strip().lower()
        if not valor:
            raise ValueError("El usuario no puede estar vacío.")
        return valor

    @field_validator("correo")
    @classmethod
    def normalizar_correo(cls, valor: EmailStr) -> str:
        return str(valor).strip().lower()

    @field_validator("password")
    @classmethod
    def validar_password(cls, valor: str) -> str:
        if len(valor.encode("utf-8")) > 72:
            raise ValueError(
                "La contraseña no puede superar los 72 bytes."
            )
        return valor


class UsuarioActualizarRequest(BaseModel):
    """Campos modificables de un usuario."""

    nombres: str | None = Field(default=None, min_length=2, max_length=100)
    apellidos: str | None = Field(default=None, min_length=2, max_length=100)
    nombre_usuario: str | None = Field(default=None, min_length=3, max_length=50)
    correo: EmailStr | None = None
    telefono: str | None = Field(default=None, max_length=20)
    documento: str | None = Field(default=None, max_length=30)
    id_barrio: int | None = None
    estado: str | None = Field(
        default=None,
        pattern="^(activo|inactivo)$",
    )

    @field_validator("nombres", "apellidos")
    @classmethod
    def limpiar_nombres(cls, valor: str | None) -> str | None:
        if valor is None:
            raise ValueError("Este campo no puede ser nulo.")

        valor = valor.strip()
        if not valor:
            raise ValueError("Este campo no puede estar vacío.")
        return valor

    @field_validator("nombre_usuario")
    @classmethod
    def normalizar_usuario(cls, valor: str | None) -> str | None:
        if valor is None:
            raise ValueError("El nombre de usuario no puede ser nulo.")
        return valor.strip().lower()

    @field_validator("correo")
    @classmethod
    def normalizar_correo(
        cls,
        valor: EmailStr | None,
    ) -> str | None:
        if valor is None:
            raise ValueError("El correo no puede ser nulo.")
        return str(valor).strip().lower()


class PerfilAsignarRequest(BaseModel):
    """Datos para cambiar el rol y crear un nuevo perfil."""

    id_rol: int = Field(gt=0)
    fecha_inicio: date
    cargo: str | None = Field(default=None, min_length=2, max_length=50)

    @field_validator("cargo")
    @classmethod
    def limpiar_cargo(cls, valor: str | None) -> str | None:
        if valor is None:
            return None

        valor = valor.strip()
        if not valor:
            return None
        return valor


class PerfilResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_perfil: UUID
    id_usuario: UUID
    id_rol: int
    fecha_inicio: date
    fecha_fin: date | None
    estado: str
    nombre_rol: str


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: UUID
    nombres: str
    apellidos: str
    nombre_completo: str | None
    nombre_usuario: str
    correo: EmailStr
    telefono: str | None
    documento: str | None
    id_barrio: int | None
    estado: str
    fecha_registro: datetime


class UsuarioDetalleResponse(UsuarioResponse):
    perfiles: list[PerfilResponse] = Field(default_factory=list)


class RolResponse(BaseModel):
    id_rol: int
    nombre_rol: RolEnum
    estado: str


class RolListadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_rol: int
    nombre_rol: str


class PerfilListadoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_perfil: UUID
    fecha_inicio: date
    fecha_fin: date | None
    estado: str
    rol: RolListadoResponse


class UsuarioListadoItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: UUID
    nombres: str
    apellidos: str
    nombre_completo: str | None
    nombre_usuario: str
    correo: EmailStr
    documento: str | None
    estado: str
    fecha_registro: datetime
    perfiles: list[PerfilListadoResponse] = Field(
        default_factory=list
    )


class PaginacionResponse(BaseModel):
    pagina: int
    por_pagina: int
    total_registros: int
    total_paginas: int


class UsuarioListadoResponse(BaseModel):
    success: bool = True
    data: list[UsuarioListadoItem]
    paginacion: PaginacionResponse
