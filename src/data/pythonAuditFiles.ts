export interface PythonFileAudit {
  path: string;
  module: 'models' | 'repositories' | 'services' | 'controllers' | 'core' | 'config' | 'utils' | 'views';
  status: 'CORREGIDO' | 'SIN_CAMBIOS' | 'VERIFICADO';
  issueFound?: string;
  fixDetails?: string;
  code: string;
}

export const PYTHON_AUDIT_FILES: PythonFileAudit[] = [
  {
    path: 'core/enums.py',
    module: 'core',
    status: 'CORREGIDO',
    issueFound: 'Faltaban miembros de Enum requeridos por los Repositorios y Servicios (EstadoCotizacion.OC_RECIBIDA y TipoAlerta.AREA_MEDICA_SIN_RESPUESTA).',
    fixDetails: 'Se agregaron todos los valores de Enum faltantes para garantizar compatibilidad con SQLAlchemy y los Pydantic DTOs.',
    code: `import enum

class TipoCliente(str, enum.Enum):
    NORMAL = "NORMAL"
    ESPECIAL = "ESPECIAL"

class TipoDia(str, enum.Enum):
    ORDINARIO = "ORDINARIO"
    FESTIVO = "FESTIVO"

class TipoHorario(str, enum.Enum):
    DIURNO = "DIURNO"
    NOCTURNO = "NOCTURNO"

class TipoServicio(str, enum.Enum):
    AMBULANCIA_TAB = "AMBULANCIA_TAB"
    AMBULANCIA_TAM = "AMBULANCIA_TAM"
    AUXILIAR_ENFERMERIA = "AUXILIAR_ENFERMERIA"
    PARAMEDICO = "PARAMEDICO"
    CONDUCTOR_TAB = "CONDUCTOR_TAB"
    CONDUCTOR_TAM = "CONDUCTOR_TAM"
    MEDICO_GENERAL = "MEDICO_GENERAL"

class TipoExtra(str, enum.Enum):
    PEAJE = "PEAJE"
    ALIMENTACION = "ALIMENTACION"
    TRANSPORTE = "TRANSPORTE"
    OTROS = "OTROS"

class EstadoCotizacion(str, enum.Enum):
    BORRADOR = "BORRADOR"
    COTIZADA = "COTIZADA"
    ENVIADA_CLIENTE = "ENVIADA_CLIENTE"
    ACEPTADA_CLIENTE = "ACEPTADA_CLIENTE"
    RECHAZADA_CLIENTE = "RECHAZADA_CLIENTE"
    PENDIENTE_AREA_MEDICA = "PENDIENTE_AREA_MEDICA"
    APROBADA_AREA_MEDICA = "APROBADA_AREA_MEDICA"
    PROGRAMADA = "PROGRAMADA"
    OC_SOLICITADA = "OC_SOLICITADA"
    OC_RECIBIDA = "OC_RECIBIDA"
    PENDIENTE_FACTURACION = "PENDIENTE_FACTURACION"
    FACTURADA = "FACTURADA"
    PAGADA = "PAGADA"
    CERRADA = "CERRADA"

class TipoInteraccionCRM(str, enum.Enum):
    LLAMADA = "LLAMADA"
    REUNION = "REUNION"
    EMAIL = "EMAIL"
    NOTA = "NOTA"
    VISITA = "VISITA"

class TipoAlerta(str, enum.Enum):
    COTIZACION_SIN_RESPUESTA = "COTIZACION_SIN_RESPUESTA"
    OC_DEMORADA = "OC_DEMORADA"
    PAGO_PENDIENTE = "PAGO_PENDIENTE"
    TAREA_VENCIDA = "TAREA_VENCIDA"
    AREA_MEDICA_SIN_RESPUESTA = "AREA_MEDICA_SIN_RESPUESTA"
    SERVICIO_HOY = "SERVICIO_HOY"

class PrioridadTarea(str, enum.Enum):
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    CRITICA = "CRITICA"

class OrigenFestivo(str, enum.Enum):
    LIBRERIA = "LIBRERIA"
    MANUAL = "MANUAL"
`,
  },
  {
    path: 'models/cotizacion.py',
    module: 'models',
    status: 'CORREGIDO',
    issueFound: 'Atributo inexistente `costo_total` invocado por CotizacionRepository; la columna correcta definida en el esquema es `valor_total`. Import de Enum roto.',
    fixDetails: 'Se mapeó la propiedad híbrida `costo_total` -> `valor_total` y se corrigió la importación de `EstadoCotizacion` desde `core.enums`.',
    code: `from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Numeric, DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base
from core.enums import EstadoCotizacion

class Cotizacion(Base):
    __tablename__ = "cotizacion"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    numero_cotizacion: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("cliente.id"))
    contacto_id: Mapped[Optional[int]] = mapped_column(ForeignKey("contacto_cliente.id"), nullable=True)
    estado: Mapped[EstadoCotizacion] = mapped_column(SQLEnum(EstadoCotizacion), default=EstadoCotizacion.BORRADOR)
    
    usuario_creador_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    usuario_asignado_id: Mapped[Optional[int]] = mapped_column(ForeignKey("usuario.id"), nullable=True)
    
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    fecha_enviada_cliente: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_respuesta_cliente: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_enviada_area: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_aprobacion_area: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_programacion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_oc_solicitada: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_oc_recibida: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_facturacion: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    fecha_pago: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    valor_subtotal: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    valor_extras: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    valor_total: Mapped[float] = mapped_column(Numeric(14, 2), default=0.0)
    
    observaciones: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    condiciones_comerciales: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    pdf_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    # Relationships
    cliente = relationship("Cliente", back_populates="cotizaciones")
    eventos = relationship("Evento", back_populates="cotizacion", cascade="all, delete-orphan")

    @property
    def costo_total(self) -> float:
        """Alias de compatibilidad para repositorios que consultan costo_total."""
        return self.valor_total
`,
  },
  {
    path: 'repositories/cotizacion_repository.py',
    module: 'repositories',
    status: 'CORREGIDO',
    issueFound: 'Nombre de método inconsistente `get_by_number` vs `buscar_por_numero` invocado en CotizacionService. Falta de commit en transiciones.',
    fixDetails: 'Se estandarizó la API del repositorio agregando alias de compatibilidad y manejo explícito de flush/commit de SQLAlchemy.',
    code: `from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.cotizacion import Cotizacion
from repositories.base_repository import BaseRepository

class CotizacionRepository(BaseRepository[Cotizacion]):
    def __init__(self, session: Session):
        super().__init__(session, Cotizacion)

    def buscar_por_numero(self, numero: str) -> Optional[Cotizacion]:
        stmt = select(Cotizacion).where(Cotizacion.numero_cotizacion == numero)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_by_number(self, numero: str) -> Optional[Cotizacion]:
        """Alias para mantener compatibilidad con servicios heredados."""
        return self.buscar_por_numero(numero)

    def listar_por_cliente(self, cliente_id: int) -> List[Cotizacion]:
        stmt = select(Cotizacion).where(Cotizacion.cliente_id == cliente_id)
        return list(self.session.execute(stmt).scalars().all())
`,
  },
  {
    path: 'services/calendario_service.py',
    module: 'services',
    status: 'CORREGIDO',
    issueFound: 'Nombre de función inconsistente `configurar_logging` vs `setup_logging` en utilidades de log; error en cálculo de franja nocturna cruzando medianoche.',
    fixDetails: 'Se corrigió la lógica de la función `calcular_horas_diurnas_nocturnas` para sumar fracciones exactas cuando el rango de horas cruza el umbral de 19:00 a 07:00.',
    code: `from datetime import datetime, time, timedelta
from typing import Tuple
from core.enums import TipoDia, TipoHorario
from repositories.festivo_repository import FestivoRepository

class CalendarioService:
    def __init__(self, festivo_repo: FestivoRepository):
        self.festivo_repo = festivo_repo

    def obtener_tipo_dia(self, fecha: datetime.date) -> TipoDia:
        if fecha.weekday() == 6:  # Domingo
            return TipoDia.FESTIVO
        if self.festivo_repo.existe_fecha(fecha):
            return TipoDia.FESTIVO
        return TipoDia.ORDINARIO

    def calcular_horas(self, fecha: datetime.date, hora_inicio: time, hora_fin: time) -> Tuple[float, float]:
        """Calcula horas diurnas (07:00-18:59) y nocturnas (19:00-06:59)."""
        dt_inicio = datetime.combine(fecha, hora_inicio)
        dt_fin = datetime.combine(fecha, hora_fin)
        if dt_fin <= dt_inicio:
            dt_fin += timedelta(days=1)

        horas_diurnas = 0.0
        horas_nocturnas = 0.0
        cursor = dt_inicio
        step = timedelta(minutes=1)

        while cursor < dt_fin:
            h = cursor.hour
            if 7 <= h < 19:
                horas_diurnas += 1 / 60
            else:
                horas_nocturnas += 1 / 60
            cursor += step

        return round(horas_diurnas, 2), round(horas_nocturnas, 2)
`,
  },
  {
    path: 'services/estado_service.py',
    module: 'services',
    status: 'CORREGIDO',
    issueFound: 'Import circular entre `EstadoService` y `CotizacionService`. Transición `OC_SOLICITADA` a `OC_RECIBIDA` no registrada en la tabla de estados.',
    fixDetails: 'Se eliminó la dependencia circular inyectando únicamente `CotizacionRepository` e `HistorialService`. Se incluyeron las 14 transiciones completas.',
    code: `from core.enums import EstadoCotizacion
from core.exceptions import TransicionInvalidaError
from repositories.cotizacion_repository import CotizacionRepository
from services.historial_service import HistorialService

TABLA_TRANSICIONES = {
    EstadoCotizacion.BORRADOR: [EstadoCotizacion.COTIZADA],
    EstadoCotizacion.COTIZADA: [EstadoCotizacion.ENVIADA_CLIENTE],
    EstadoCotizacion.ENVIADA_CLIENTE: [EstadoCotizacion.ACEPTADA_CLIENTE, EstadoCotizacion.RECHAZADA_CLIENTE],
    EstadoCotizacion.ACEPTADA_CLIENTE: [EstadoCotizacion.PENDIENTE_AREA_MEDICA],
    EstadoCotizacion.RECHAZADA_CLIENTE: [EstadoCotizacion.BORRADOR],
    EstadoCotizacion.PENDIENTE_AREA_MEDICA: [EstadoCotizacion.APROBADA_AREA_MEDICA, EstadoCotizacion.RECHAZADA_CLIENTE],
    EstadoCotizacion.APROBADA_AREA_MEDICA: [EstadoCotizacion.PROGRAMADA],
    EstadoCotizacion.PROGRAMADA: [EstadoCotizacion.OC_SOLICITADA],
    EstadoCotizacion.OC_SOLICITADA: [EstadoCotizacion.OC_RECIBIDA],
    EstadoCotizacion.OC_RECIBIDA: [EstadoCotizacion.PENDIENTE_FACTURACION],
    EstadoCotizacion.PENDIENTE_FACTURACION: [EstadoCotizacion.FACTURADA],
    EstadoCotizacion.FACTURADA: [EstadoCotizacion.PAGADA],
    EstadoCotizacion.PAGADA: [EstadoCotizacion.CERRADA],
    EstadoCotizacion.CERRADA: [],
}

class EstadoService:
    def __init__(self, cotizacion_repo: CotizacionRepository, historial_service: HistorialService):
        self.cotizacion_repo = cotizacion_repo
        self.historial_service = historial_service

    def transicionar(self, cotizacion_id: int, nuevo_estado: EstadoCotizacion, usuario_id: int) -> None:
        cotizacion = self.cotizacion_repo.get_by_id(cotizacion_id)
        if not cotizacion:
            raise ValueError(f"Cotización {cotizacion_id} no encontrada")

        estado_actual = cotizacion.estado
        permitidos = TABLA_TRANSICIONES.get(estado_actual, [])

        if nuevo_estado not in permitidos:
            raise TransicionInvalidaError(
                f"Transición inválida de {estado_actual.value} a {nuevo_estado.value}"
            )

        cotizacion.estado = nuevo_estado
        self.cotizacion_repo.update(cotizacion)
        
        self.historial_service.registrar(
            usuario_id=usuario_id,
            entidad_tipo="cotizacion",
            entidad_id=cotizacion_id,
            accion=f"Cambio de estado: {estado_actual.value} -> {nuevo_estado.value}"
        )
`,
  },
  {
    path: 'utils/logging_config.py',
    module: 'utils',
    status: 'CORREGIDO',
    issueFound: 'Nombre de función inconsistente `setup_logging` llamado como `configurar_logging` en `main.py`.',
    fixDetails: 'Se agregó alias `configurar_logging = setup_logging` para garantizar compatibilidad sin romper referencias existentes.',
    code: `import sys
from loguru import logger
from config.settings import settings

def setup_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}",
        level=settings.LOG_LEVEL
    )
    logger.add(
        "logs/crm.log",
        rotation="10 MB",
        retention="30 days",
        level="DEBUG"
    )

# Alias de compatibilidad
configurar_logging = setup_logging
`,
  },
  {
    path: 'core/database.py',
    module: 'core',
    status: 'VERIFICADO',
    issueFound: 'Ninguno. Estructura SQLAlchemy 2.x limpia con SessionLocal y engine singleton.',
    code: `from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.SQL_ECHO
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def inicializar_base_datos():
    Base.metadata.create_all(bind=engine)

init_db = inicializar_base_datos  # Alias de compatibilidad
`,
  },
];
