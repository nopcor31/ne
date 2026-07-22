"""
Enumeraciones del dominio del negocio.

Define todos los valores constantes y estados del sistema CRM Operativo
conforme a la especificacion del documento de arquitectura.
"""

from enum import Enum


class TipoCliente(str, Enum):
    """Tipo de cliente para categorizacion y aplicacion de tarifas."""
    NORMAL = "NORMAL"
    ESPECIAL = "ESPECIAL"


class TipoDia(str, Enum):
    """Clasificacion de dias para calculo tarifario."""
    ORDINARIO = "ORDINARIO"  # Lunes a Sabado no festivo
    FESTIVO = "FESTIVO"      # Domingos y festivos legales


class TipoHorario(str, Enum):
    """Franja horaria para asignacion de tarifas de servicio."""
    DIURNO = "DIURNO"      # 07:00 - 18:59
    NOCTURNO = "NOCTURNO"  # 19:00 - 06:59


class TipoServicio(str, Enum):
    """Servicios medicos y ambulatorios prestados por la organizacion."""
    AMBULANCIA_TAB = "AMBULANCIA_TAB"
    AMBULANCIA_TAM = "AMBULANCIA_TAM"
    AUXILIAR_ENFERMERIA = "AUXILIAR_ENFERMERIA"
    PARAMEDICO = "PARAMEDICO"
    CONDUCTOR_TAB = "CONDUCTOR_TAB"
    CONDUCTOR_TAM = "CONDUCTOR_TAM"
    MEDICO_GENERAL = "MEDICO_GENERAL"


class TipoExtra(str, Enum):
    """Costos adicionales o insumos imputables a un evento."""
    PEAJE = "PEAJE"
    ALIMENTACION = "ALIMENTACION"
    TRANSPORTE = "TRANSPORTE"
    OTROS = "OTROS"


class EstadoCotizacion(str, Enum):
    """
    Maquina de estados completa de la cotizacion (14 estados).
    Gobierna el ciclo de vida comercial y operativo del expediente.
    """
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


class TipoInteraccionCRM(str, Enum):
    """Puntos de contacto registrados con el cliente."""
    LLAMADA = "LLAMADA"
    REUNION = "REUNION"
    EMAIL = "EMAIL"
    NOTA = "NOTA"
    VISITA = "VISITA"


class TipoAlerta(str, Enum):
    """Tipos de alertas generadas automaticamente por el sistema."""
    COTIZACION_SIN_RESPUESTA = "COTIZACION_SIN_RESPUESTA"
    AREA_MEDICA_SIN_RESPUESTA = "AREA_MEDICA_SIN_RESPUESTA"
    OC_DEMORADA = "OC_DEMORADA"
    PAGO_PENDIENTE = "PAGO_PENDIENTE"
    TAREA_VENCIDA = "TAREA_VENCIDA"
    SERVICIO_HOY = "SERVICIO_HOY"


class PrioridadTarea(str, Enum):
    """Nivel de urgencia asignado a una tarea CRM."""
    BAJA = "BAJA"
    MEDIA = "MEDIA"
    ALTA = "ALTA"
    CRITICA = "CRITICA"


class PrioridadAlerta(str, Enum):
    """Severidad de una alerta para despliegue visual."""
    INFO = "INFO"
    ADVERTENCIA = "ADVERTENCIA"
    CRITICA = "CRITICA"


class OrigenFestivo(str, Enum):
    """Origen del registro de dia festivo."""
    LIBRERIA = "LIBRERIA"
    MANUAL = "MANUAL"


class EstadoProgramacion(str, Enum):
    """Estado operativo del servicio programado en agenda."""
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    REALIZADA = "REALIZADA"
    CANCELADA = "CANCELADA"


class EstadoOrdenCompra(str, Enum):
    """Estado de recepcion de la Orden de Compra del cliente."""
    SOLICITADA = "SOLICITADA"
    RECIBIDA = "RECIBIDA"


class EstadoFactura(str, Enum):
    """Estado de cobro de la factura emitida."""
    PENDIENTE = "PENDIENTE"
    FACTURADA = "FACTURADA"
    PAGADA = "PAGADA"
