
from datetime import date
from math import ceil
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.administracion_repository import (
    AdministracionRepository,
)
from src.schemas.usuario import (
    UsuarioAdminCreate,
    UsuarioAdminCreateResponse,
    UsuarioAdminData,
    PerfilUsuarioResponse,
    RolUsuarioResponse,
)
from src.schemas.administracion import (
    UsuarioActualizarRequest,
    PerfilAsignarRequest,
    UsuarioListadoItem,
    UsuarioListadoResponse,
    PaginacionResponse,
    RolResponse,
)
from src.security.password import hashear_password


class AdministracionService:
    """Lógica de negocio para la gestión administrativa de usuarios."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def listar_roles(self, solo_activos: bool = True):
        """Consulta los roles disponibles para administración."""

        roles = await AdministracionRepository.listar_roles(
            self.db,
            solo_activos=solo_activos,
        )

        return {
            "success": True,
            "data": [
                RolResponse(
                    id_rol=rol.id_rol,
                    nombre_rol=rol.nombre_rol,
                    estado=rol.estado,
                )
                for rol in roles
            ],
        }

    async def registrar_usuario(
        self,
        datos: UsuarioAdminCreate,
    ) -> UsuarioAdminCreateResponse:
        correo = str(datos.correo).strip().lower()
        nombre_usuario = datos.nombre_usuario.strip()
        documento = datos.perfil.documento.strip()

        if await AdministracionRepository.buscar_por_correo(
            self.db, correo
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "EMAIL_ALREADY_EXISTS",
                    "message": "El correo electrónico ya está registrado.",
                    "details": {"field": "correo"},
                },
            )

        if await AdministracionRepository.buscar_por_nombre_usuario(
            self.db, nombre_usuario
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "USERNAME_ALREADY_EXISTS",
                    "message": "El nombre de usuario ya está registrado.",
                    "details": {"field": "nombre_usuario"},
                },
            )

        if await AdministracionRepository.buscar_por_documento(
            self.db, documento
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "DOCUMENT_ALREADY_EXISTS",
                    "message": "El documento ya está registrado.",
                    "details": {"field": "perfil.documento"},
                },
            )

        rol = await AdministracionRepository.obtener_rol_por_id(
            self.db, datos.perfil.rol_id
        )

        if not rol:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "code": "INVALID_ROLE",
                    "message": (
                        "El rol seleccionado no existe o está inactivo."
                    ),
                    "details": {"field": "perfil.rol_id"},
                },
            )

        es_trabajador = rol.nombre_rol.strip().lower() == "trabajador"

        if es_trabajador and not datos.perfil.cargo:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "code": "CARGO_REQUIRED",
                    "message": (
                        "El cargo es obligatorio para el rol trabajador."
                    ),
                    "details": {"field": "perfil.cargo"},
                },
            )

        password_hash = hashear_password(datos.password)

        try:
            usuario, perfil, _trabajador = (
                await AdministracionRepository.crear_usuario_con_perfil(
                    self.db,
                    nombres=datos.nombres,
                    apellidos=datos.apellidos,
                    nombre_usuario=nombre_usuario,
                    correo=correo,
                    password_hash=password_hash,
                    documento=documento,
                    rol=rol,
                    fecha_inicio=datos.perfil.fecha_inicio,
                    perfil_activo=datos.perfil.estado,
                    cargo=datos.perfil.cargo,
                )
            )
            await self.db.commit()

        except IntegrityError as error:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "REGISTRATION_CONFLICT",
                    "message": (
                        "No fue posible registrar el usuario porque "
                        "alguno de sus datos ya está registrado."
                    ),
                },
            ) from error

        except Exception:
            await self.db.rollback()
            raise

        return UsuarioAdminCreateResponse(
            success=True,
            message="Usuario registrado correctamente",
            data=UsuarioAdminData(
                id=usuario.id_usuario,
                nombres=usuario.nombres,
                apellidos=usuario.apellidos,
                nombre_usuario=usuario.nombre_usuario,
                correo=usuario.correo,
                activo=usuario.estado == "activo",
                perfil=PerfilUsuarioResponse(
                    id=perfil.id_perfil,
                    documento=documento,
                    fecha_inicio=perfil.fecha_inicio,
                    estado=perfil.estado == "activo",
                    rol=RolUsuarioResponse(
                        id=rol.id_rol,
                        nombre=rol.nombre_rol,
                    ),
                ),
            ),
        )

    async def listar_usuarios(
        self,
        pagina: int = 1,
        por_pagina: int = 10,
    ) -> UsuarioListadoResponse:
        if pagina < 1 or por_pagina < 1 or por_pagina > 100:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Parámetros de paginación inválidos.",
            )

        usuarios, total = (
            await AdministracionRepository.listar_usuarios(
                self.db,
                offset=(pagina - 1) * por_pagina,
                limit=por_pagina,
            )
        )

        return UsuarioListadoResponse(
            success=True,
            data=[
                UsuarioListadoItem.model_validate(usuario)
                for usuario in usuarios
            ],
            paginacion=PaginacionResponse(
                pagina=pagina,
                por_pagina=por_pagina,
                total_registros=total,
                total_paginas=ceil(total / por_pagina) if total else 0,
            ),
        )

    async def obtener_usuario_por_id(
        self,
        id_usuario: UUID,
    ) -> UsuarioListadoItem:
        usuario = (
            await AdministracionRepository.buscar_usuario_por_id(
                self.db, id_usuario
            )
        )

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "USER_NOT_FOUND",
                    "message": "No se encontró el usuario solicitado.",
                },
            )

        return UsuarioListadoItem.model_validate(usuario)

    async def actualizar_usuario(
        self,
        id_usuario: UUID,
        datos: UsuarioActualizarRequest,
    ) -> UsuarioListadoItem:
        usuario = (
            await AdministracionRepository.buscar_usuario_por_id(
                self.db, id_usuario
            )
        )

        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "USER_NOT_FOUND",
                    "message": "No se encontró el usuario solicitado.",
                },
            )

        cambios = datos.model_dump(exclude_unset=True)

        if not cambios:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "EMPTY_UPDATE",
                    "message": "Debes enviar al menos un campo.",
                },
            )

        validaciones = (
            ("correo", "buscar_por_correo", "EMAIL_ALREADY_EXISTS"),
            (
                "nombre_usuario",
                "buscar_por_nombre_usuario",
                "USERNAME_ALREADY_EXISTS",
            ),
            ("documento", "buscar_por_documento", "DOCUMENT_ALREADY_EXISTS"),
        )

        for campo, metodo, codigo in validaciones:
            valor = cambios.get(campo)

            if valor is None:
                continue

            existente = await getattr(
                AdministracionRepository, metodo
            )(self.db, valor)

            if (
                existente is not None
                and existente.id_usuario != id_usuario
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "code": codigo,
                        "message": f"El campo {campo} ya está registrado.",
                        "details": {"field": campo},
                    },
                )

        try:
            await AdministracionRepository.actualizar_usuario(
                self.db, usuario, cambios
            )
            await self.db.commit()

        except IntegrityError as error:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "UPDATE_CONFLICT",
                    "message": (
                        "No fue posible actualizar el usuario. "
                        "Verifica los datos y el barrio seleccionado."
                    ),
                },
            ) from error

        except Exception:
            await self.db.rollback()
            raise

        actualizado = (
            await AdministracionRepository.buscar_usuario_por_id(
                self.db, id_usuario
            )
        )

        return UsuarioListadoItem.model_validate(actualizado)

    async def cambiar_rol_usuario(
        self,
        id_usuario: UUID,
        datos: PerfilAsignarRequest,
    ) -> UsuarioListadoItem:
        """Cierra el perfil actual y crea uno nuevo conservando historial."""

        try:
            usuario = (
                await AdministracionRepository
                .obtener_usuario_para_cambio_perfil(
                    self.db,
                    id_usuario,
                )
            )

            if usuario is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={
                        "code": "USER_NOT_FOUND",
                        "message": "No se encontró el usuario solicitado.",
                    },
                )

            if usuario.estado != "activo":
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "code": "USER_INACTIVE",
                        "message": (
                            "No se puede cambiar el rol de un usuario "
                            "inactivo."
                        ),
                    },
                )

            nuevo_rol = (
                await AdministracionRepository.obtener_rol_por_id(
                    self.db,
                    datos.id_rol,
                )
            )

            if nuevo_rol is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={
                        "code": "INVALID_ROLE",
                        "message": "El rol no existe o está inactivo.",
                        "details": {"field": "id_rol"},
                    },
                )

            es_trabajador = (
                nuevo_rol.nombre_rol.strip().lower() == "trabajador"
            )

            if es_trabajador and not datos.cargo:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={
                        "code": "CARGO_REQUIRED",
                        "message": (
                            "El cargo es obligatorio para el rol trabajador."
                        ),
                        "details": {"field": "cargo"},
                    },
                )

            if not es_trabajador and datos.cargo:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={
                        "code": "CARGO_NOT_ALLOWED",
                        "message": (
                            "El cargo solamente se envía para el rol "
                            "trabajador."
                        ),
                        "details": {"field": "cargo"},
                    },
                )

            perfiles_activos = [
                perfil
                for perfil in usuario.perfiles
                if perfil.estado == "activo" and perfil.fecha_fin is None
            ]

            if len(perfiles_activos) > 1:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "code": "MULTIPLE_ACTIVE_PROFILES",
                        "message": (
                            "El usuario tiene más de un perfil activo. "
                            "Debe corregirse antes de cambiar su rol."
                        ),
                    },
                )

            perfil_actual = (
                perfiles_activos[0] if perfiles_activos else None
            )

            if (
                perfil_actual is not None
                and perfil_actual.id_rol == nuevo_rol.id_rol
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail={
                        "code": "ROLE_ALREADY_ASSIGNED",
                        "message": "El usuario ya tiene asignado ese rol.",
                    },
                )

            if datos.fecha_inicio > date.today():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail={
                        "code": "INVALID_START_DATE",
                        "message": "La fecha de inicio no puede ser futura.",
                        "details": {"field": "fecha_inicio"},
                    },
                )

            if perfil_actual is not None:
                if datos.fecha_inicio < perfil_actual.fecha_inicio:
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail={
                            "code": "INVALID_START_DATE",
                            "message": (
                                "La fecha de inicio del nuevo perfil "
                                "no puede ser anterior al perfil actual."
                            ),
                            "details": {"field": "fecha_inicio"},
                        },
                    )

                perfil_actual.estado = "inactivo"
                perfil_actual.fecha_fin = datos.fecha_inicio

                trabajador_anterior = perfil_actual.trabajador

                if trabajador_anterior is not None:
                    trabajador_anterior.estado = "inactivo"

            await AdministracionRepository.crear_perfil(
                self.db,
                usuario=usuario,
                rol=nuevo_rol,
                fecha_inicio=datos.fecha_inicio,
                cargo=datos.cargo,
            )

            await self.db.commit()

        except HTTPException:
            await self.db.rollback()
            raise

        except IntegrityError as error:
            await self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "PROFILE_CHANGE_CONFLICT",
                    "message": (
                        "No fue posible cambiar el perfil. "
                        "Verifica las restricciones de la base de datos."
                    ),
                },
            ) from error

        except Exception:
            await self.db.rollback()
            raise

        usuario_actualizado = (
            await AdministracionRepository.buscar_usuario_por_id(
                self.db,
                id_usuario,
            )
        )

        return UsuarioListadoItem.model_validate(usuario_actualizado)
