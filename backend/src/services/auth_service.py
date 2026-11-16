
import uuid

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.models import Usuario
from src.repository.usuario_repository import (
    ESTADO_ACTIVO,
    UsuarioRepository,
)
from src.schemas.auth import (
    LoginRequest,
    RegistroRequest,
    RegistroResponse,
    RolEnum,
    TokenResponse,
    UsuarioActualResponse,
)
from src.security.password import (
    hashear_password,
    verificar_password,
)
from src.security.tokens import crear_access_token


class AuthService:
    """Lógica de negocio de autenticación y registro."""

    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    async def registrar(
        self,
        datos: RegistroRequest,
    ) -> RegistroResponse:
        """Registra un ciudadano sin permitir elegir su rol."""

        correo = str(datos.correo).lower()
        nombre_usuario = datos.nombre_usuario.lower()

        if await self.usuario_repository.buscar_por_correo(correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo electrónico ya está registrado.",
            )

        if await self.usuario_repository.buscar_por_nombre_usuario(
            nombre_usuario
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El nombre de usuario ya está registrado.",
            )

        perfil = await self.usuario_repository.obtener_perfil_por_rol(
            RolEnum.CIUDADANO.value
        )

        if not perfil:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "No existe un perfil activo para el rol ciudadano. "
                    "Verifica la inicialización de los roles."
                ),
            )

        password_hash = hashear_password(datos.password)

        try:
            usuario = (
                await self.usuario_repository.crear_usuario_ciudadano(
                    nombres=datos.nombres,
                    apellidos=datos.apellidos,
                    nombre_usuario=nombre_usuario,
                    correo=correo,
                    password_hash=password_hash,
                    telefono=datos.telefono,
                    perfil=perfil,
                )
            )

            await self.usuario_repository.db.commit()
            await self.usuario_repository.db.refresh(usuario)

        except IntegrityError:
            await self.usuario_repository.db.rollback()

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    "El correo, nombre de usuario o documento "
                    "ya se encuentra registrado."
                ),
            )

        return RegistroResponse(
            id=str(usuario.id_usuario),
            nombre=(
                usuario.nombre_completo
                or f"{usuario.nombres} {usuario.apellidos}"
            ),
            email=usuario.correo,
            rol=RolEnum.CIUDADANO,
            mensaje="Usuario registrado correctamente.",
        )

    async def login(self, datos: LoginRequest) -> TokenResponse:
        usuario = (
            await self.usuario_repository.buscar_por_correo_o_usuario(
                datos.identificador.strip()
            )
        )

        if not usuario or not verificar_password(
            datos.password,
            usuario.password_hash,
        ):
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Credenciales inválidas",
            )

        if usuario.estado != ESTADO_ACTIVO:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Usuario inactivo",
            )

        rol = await self._obtener_rol(usuario.id_usuario)

        return TokenResponse(
            access_token=crear_access_token(
                str(usuario.id_usuario),
                rol.value,
            )
        )

    async def obtener_usuario_actual(
        self,
        id_usuario: str,
    ) -> UsuarioActualResponse:
        usuario = await self._buscar_usuario_activo(id_usuario)
        rol = await self._obtener_rol(usuario.id_usuario)

        return UsuarioActualResponse(
            id=str(usuario.id_usuario),
            nombre=(
                usuario.nombre_completo
                or f"{usuario.nombres} {usuario.apellidos}"
            ),
            email=usuario.correo,
            rol=rol,
        )

    async def _buscar_usuario_activo(
        self,
        id_usuario: str,
    ) -> Usuario:
        try:
            usuario = (
                await self.usuario_repository.buscar_por_id(
                    uuid.UUID(id_usuario)
                )
            )
        except ValueError:
            usuario = None

        if not usuario or usuario.estado != ESTADO_ACTIVO:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return usuario

    async def _obtener_rol(
        self,
        id_usuario: uuid.UUID,
    ) -> RolEnum:
        nombre_rol = (
            await self.usuario_repository.obtener_rol_activo(
                id_usuario
            )
        )

        try:
            return RolEnum(nombre_rol)
        except ValueError:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN,
                "Usuario sin rol activo",
            )
