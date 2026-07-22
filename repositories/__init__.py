"""
Paquete de repositorios para acceso a datos desacoplado.
"""

from repositories.base_repository import BaseRepository
from repositories.usuario_repository import UsuarioRepository
from repositories.cliente_repository import ClienteRepository
from repositories.contacto_repository import ContactoRepository
from repositories.interaccion_repository import InteraccionRepository
from repositories.tarea_repository import TareaRepository
from repositories.ciudad_repository import CiudadRepository
from repositories.servicio_repository import ServicioRepository
from repositories.festivo_repository import FestivoRepository
from repositories.tarifa_repository import TarifaRepository
from repositories.cotizacion_repository import CotizacionRepository
from repositories.evento_repository import EventoRepository
from repositories.extra_evento_repository import ExtraEventoRepository
from repositories.area_medica_repository import AreaMedicaRepository
from repositories.envio_area_medica_repository import EnvioAreaMedicaRepository
from repositories.programacion_repository import ProgramacionRepository
from repositories.orden_compra_repository import OrdenCompraRepository
from repositories.factura_repository import FacturaRepository
from repositories.alerta_repository import AlertaRepository
from repositories.historial_repository import HistorialRepository
from repositories.configuracion_repository import ConfiguracionRepository

__all__ = [
    "BaseRepository",
    "UsuarioRepository",
    "ClienteRepository",
    "ContactoRepository",
    "InteraccionRepository",
    "TareaRepository",
    "CiudadRepository",
    "ServicioRepository",
    "FestivoRepository",
    "TarifaRepository",
    "CotizacionRepository",
    "EventoRepository",
    "ExtraEventoRepository",
    "AreaMedicaRepository",
    "EnvioAreaMedicaRepository",
    "ProgramacionRepository",
    "OrdenCompraRepository",
    "FacturaRepository",
    "AlertaRepository",
    "HistorialRepository",
    "ConfiguracionRepository",
]
