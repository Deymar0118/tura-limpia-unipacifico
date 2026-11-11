import logging
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger("turalimpia.config")

# Identificación y Estado de la Aplicación
class Settings(BaseSettings):
    app_name: str = "TuraLimpia API"
    app_version: str = "1.0.0"
    api_v1_str: str = "/api/v1"
    debug: bool = False
    entorno: str = "desarrollo"

# Conexión al Motor Relacional PostgreSQL
    database_url: str = "sqlite+aiosqlite:///./tura_limpia.db"

    @property
    def database_url_async(self) -> str:
        url = self.database_url
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

# Seguridad y Firma de Tokens de Acceso (JWT)
    jwt_secret_key: str = "turalimpia_dev_secret_key_cambiar_en_produccion_obligatorio"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

# Configuración del Protocolo CORS (Cross-Origin Resource Sharing)
    allowed_origins: str = "http://localhost:5173"

# Parámetros de Ingesta del Archivo de Entorno
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def es_produccion(self) -> bool:
        return self.entorno.lower() == "produccion"

    def validar_produccion(self) -> None:
        if (
            self.es_produccion
            and "dev_secret" in self.jwt_secret_key.lower()
        ):
            raise RuntimeError(
                "JWT_SECRET_KEY no cumple con las políticas de seguridad para producción."
            )
        if self.es_produccion and len(self.jwt_secret_key) < 32:
            raise RuntimeError(
                "JWT_SECRET_KEY debe tener al menos 32 caracteres en producción."
            )
        if self.es_produccion and self.allowed_origins.strip() == "*":
            raise RuntimeError(
                "ALLOWED_ORIGINS requiere un dominio específico en producción."
            )


@lru_cache
def get_settings() -> Settings:
    return Settings()