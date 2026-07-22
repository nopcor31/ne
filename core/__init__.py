"""
Paquete core de la aplicacion CRM Operativo.
"""

from core.database import Base, engine, SessionLocal, inicializar_base_datos, get_db
from core.session_manager import session_manager
from core.enums import (
    TipoCliente,
    TipoDia,
    TipoHorario,
    TipoServicio,
    TipoExtra,
    EstadoCotizacion,
    TipoInteraccionCRM,
    TipoAlerta,
    PrioridadTarea,
    PrioridadAlerta,
    OrigenFestivo,
    EstadoProgramacion,
    EstadoOrdenCompra,
    EstadoFactura,
)
from core.exceptions import (
    CRMException,
    EntidadNoEncontradaError,
    TarifaNoEncontradaError,
    TransicionInvalidaError,
    ValidacionError,
    IntegracionOutlookError,
    GeneracionPDFError,
    ReglaNegocioError,
)

__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "inicializar_base_datos",
    "get_db",
    "session_manager",
    "TipoCliente",
    "TipoDia",
    "TipoHorario",
    "TipoServicio",
    "TipoExtra",
    "EstadoCotizacion",
    "TipoInteraccionCRM",
    "TipoAlerta",
    "PrioridadTarea",
    "PrioridadAlerta",
    "OrigenFestivo",
    "EstadoProgramacion",
    "EstadoOrdenCompra",
    "EstadoFactura",
    "CRMException",
    "EntidadNoEncontradaError",
    "TarifaNoEncontradaError",
    "TransicionInvalidaError",
    "ValidacionError",
    "IntegracionOutlookError",
    "GeneracionPDFError",
    "ReglaNegocioError",
]
