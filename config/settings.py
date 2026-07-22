"""
Modulo de configuracion global para el CRM Operativo.

Proporciona rutas del sistema, constantes de la aplicacion,
configuraciones por defecto de empresa, correo y tiempos de timeout.
"""

from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracion centralizada de la aplicacion basada en Pydantic."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Informacion General de la Aplicacion
    APP_NAME: str = "CRM Operativo — Servicios Medicos NE"
    APP_VERSION: str = "2.0.0"
    ORGANIZATION_NAME: str = "Servicios Medicos NE S.A.S."

    # Rutas del Sistema
    BASE_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    DATA_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "data")
    LOGS_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "logs")
    RESOURCES_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "resources")
    OUTPUT_DIR: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent / "output")

    # Base de Datos
    DATABASE_NAME: str = "ne_crm.db"
    
    @property
    def DATABASE_PATH(self) -> Path:
        """Ruta absoluta al archivo de base de datos SQLite."""
        return self.DATA_DIR / self.DATABASE_NAME

    @property
    def DATABASE_URL(self) -> str:
        """URI de conexion SQLAlchemy para la base de datos SQLite."""
        return f"sqlite:///{self.DATABASE_PATH.as_posix()}"

    # Parametros Empresariales por Defecto
    EMPRESA_NOMBRE: str = "Servicios Medicos NE S.A.S."
    EMPRESA_NIT: str = "900.123.456-7"
    EMPRESA_DIRECCION: str = "Calle 100 # 15-20, Oficina 501, Bogota, D.C."
    EMPRESA_TELEFONO: str = "+57 (601) 745-8900"
    EMPRESA_EMAIL: str = "comercial@serviciosmedicosne.com"
    EMPRESA_SITIO_WEB: str = "www.serviciosmedicosne.com"
    EMPRESA_LOGO_PATH: str = "resources/icons/logo_ne.png"

    # Reglas de Negocio Horarias
    HORA_INICIO_DIURNO: int = 7    # 07:00
    HORA_FIN_DIURNO: int = 19     # 18:59 (19:00 es inicio nocturno)

    # Parametros de Alertas (en dias)
    DIAS_COTIZACION_SIN_RESPUESTA: int = 3
    DIAS_AREA_MEDICA_SIN_RESPUESTA: int = 2
    DIAS_OC_DEMORADA: int = 5
    INTERVALO_CHECK_ALERTAS_SEGUNDOS: int = 300  # 5 minutos

    # Integraciones
    OUTLOOK_CUENTA_EMAIL: str = ""
    PDF_CONDICIONES_GENERALES: str = (
        "1. Cotización válida por 15 días calendario a partir de la fecha de emisión.\n"
        "2. El servicio está sujeto a disponibilidad de agenda al momento de recibir la orden de compra.\n"
        "3. Cancelaciones con menos de 12 horas de anticipación generarán un cobro del 50% del valor del servicio."
    )

    def asegurar_directorios(self) -> None:
        """Crea los directorios necesarios si no existen."""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Instancia global de configuracion
settings = Settings()
settings.asegurar_directorios()
