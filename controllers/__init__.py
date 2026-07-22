"""
Paquete de controladores MVC de la aplicacion.
"""

from controllers.dashboard_controller import DashboardController
from controllers.crm_controller import CRMController
from controllers.cliente_controller import ClienteController
from controllers.tarifa_controller import TarifaController
from controllers.cotizacion_controller import CotizacionController
from controllers.evento_controller import EventoController
from controllers.programacion_controller import ProgramacionController
from controllers.area_medica_controller import AreaMedicaController
from controllers.oc_controller import OCController
from controllers.facturacion_controller import FacturacionController
from controllers.alerta_controller import AlertaController
from controllers.historial_controller import HistorialController
from controllers.configuracion_controller import ConfiguracionController

__all__ = [
    "DashboardController",
    "CRMController",
    "ClienteController",
    "TarifaController",
    "CotizacionController",
    "EventoController",
    "ProgramacionController",
    "AreaMedicaController",
    "OCController",
    "FacturacionController",
    "AlertaController",
    "HistorialController",
    "ConfiguracionController",
]
