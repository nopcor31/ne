"""
Servicio de la Maquina de Estados de Cotizacion.

Gobierna las 14 transiciones de estado permitidas del pipeline comercial
y ejecuta los efectos colaterales correspondientes a cada cambio de estado.
"""

from datetime import datetime
from typing import Dict, Set, Optional
from sqlalchemy.orm import Session
from models.cotizacion import Cotizacion
from repositories.cotizacion_repository import CotizacionRepository
from services.historial_service import HistorialService
from core.enums import EstadoCotizacion
from core.exceptions import TransicionInvalidaError
from loguru import logger


class EstadoService:
    """Maquina de estados estricta para la entidad Cotizacion."""

    # Tabla de transiciones de estado estrictamente permitidas
    TRANSICIONES_VALIDAS: Dict[EstadoCotizacion, Set[EstadoCotizacion]] = {
        EstadoCotizacion.BORRADOR: {
            EstadoCotizacion.COTIZADA
        },
        EstadoCotizacion.COTIZADA: {
            EstadoCotizacion.BORRADOR,
            EstadoCotizacion.ENVIADA_CLIENTE
        },
        EstadoCotizacion.ENVIADA_CLIENTE: {
            EstadoCotizacion.ACEPTADA_CLIENTE,
            EstadoCotizacion.RECHAZADA_CLIENTE
        },
        EstadoCotizacion.ACEPTADA_CLIENTE: {
            EstadoCotizacion.PENDIENTE_AREA_MEDICA
        },
        EstadoCotizacion.PENDIENTE_AREA_MEDICA: {
            EstadoCotizacion.APROBADA_AREA_MEDICA,
            EstadoCotizacion.RECHAZADA_CLIENTE
        },
        EstadoCotizacion.APROBADA_AREA_MEDICA: {
            EstadoCotizacion.PROGRAMADA
        },
        EstadoCotizacion.PROGRAMADA: {
            EstadoCotizacion.OC_SOLICITADA
        },
        EstadoCotizacion.OC_SOLICITADA: {
            EstadoCotizacion.OC_RECIBIDA
        },
        EstadoCotizacion.OC_RECIBIDA: {
            EstadoCotizacion.PENDIENTE_FACTURACION
        },
        EstadoCotizacion.PENDIENTE_FACTURACION: {
            EstadoCotizacion.FACTURADA
        },
        EstadoCotizacion.FACTURADA: {
            EstadoCotizacion.PAGADA
        },
        EstadoCotizacion.PAGADA: {
            EstadoCotizacion.CERRADA
        },
        EstadoCotizacion.RECHAZADA_CLIENTE: {
            EstadoCotizacion.CERRADA
        },
        EstadoCotizacion.CERRADA: set()  # Estado terminal sin transiciones salientes
    }

    def __init__(self, session: Session):
        self.session = session
        self.cotizacion_repo = CotizacionRepository(session)
        self.historial_service = HistorialService(session)

    def transicionar(
        self,
        cotizacion_id: int,
        nuevo_estado: EstadoCotizacion,
        usuario_id: int,
        observacion: Optional[str] = None
    ) -> Cotizacion:
        """
        Ejecuta la transicion de estado validando las reglas de negocio.
        
        Args:
            cotizacion_id (int): ID de la cotizacion.
            nuevo_estado (EstadoCotizacion): Estado destino solicitado.
            usuario_id (int): Usuario que realiza el cambio.
            observacion (str, optional): Nota explicativa de la transicion.
            
        Returns:
            Cotizacion: Instancia de la cotizacion con el nuevo estado aplicado.
            
        Raises:
            TransicionInvalidaError: Si la transicion no esta permitida.
        """
        cotizacion = self.cotizacion_repo.get_by_id_or_fail(cotizacion_id)
        estado_actual = cotizacion.estado

        # Validar si la transicion esta en la tabla
        destinos_permitidos = self.TRANSICIONES_VALIDAS.get(estado_actual, set())
        if nuevo_estado not in destinos_permitidos:
            logger.warning(
                f"Intento de transicion invalida en Cotizacion #{cotizacion_id}: "
                f"de {estado_actual.value} a {nuevo_estado.value}"
            )
            raise TransicionInvalidaError(estado_actual.value, nuevo_estado.value, cotizacion_id)

        # Aplicar nuevo estado y registrar estampas de tiempo segun corresponda
        ahora = datetime.now()
        cotizacion.estado = nuevo_estado

        if nuevo_estado == EstadoCotizacion.ENVIADA_CLIENTE:
            cotizacion.fecha_enviada_cliente = ahora
        elif nuevo_estado in (EstadoCotizacion.ACEPTADA_CLIENTE, EstadoCotizacion.RECHAZADA_CLIENTE):
            cotizacion.fecha_respuesta_cliente = ahora
        elif nuevo_estado == EstadoCotizacion.PENDIENTE_AREA_MEDICA:
            cotizacion.fecha_enviada_area = ahora
        elif nuevo_estado == EstadoCotizacion.APROBADA_AREA_MEDICA:
            cotizacion.fecha_aprobacion_area = ahora
        elif nuevo_estado == EstadoCotizacion.PROGRAMADA:
            cotizacion.fecha_programacion = ahora
        elif nuevo_estado == EstadoCotizacion.OC_SOLICITADA:
            cotizacion.fecha_oc_solicitada = ahora
        elif nuevo_estado == EstadoCotizacion.OC_RECIBIDA:
            cotizacion.fecha_oc_recibida = ahora
        elif nuevo_estado == EstadoCotizacion.FACTURADA:
            cotizacion.fecha_facturacion = ahora
        elif nuevo_estado == EstadoCotizacion.PAGADA:
            cotizacion.fecha_pago = ahora

        self.session.flush()

        # Registrar trazabilidad en el historial
        detalle_msg = f"Transicion de {estado_actual.value} -> {nuevo_estado.value}"
        if observacion:
            detalle_msg += f" | Obs: {observacion}"

        self.historial_service.registrar_accion(
            usuario_id=usuario_id,
            entidad_tipo="cotizacion",
            entidad_id=cotizacion.id,
            accion=f"Cambio de Estado: {nuevo_estado.value}",
            detalle=detalle_msg,
            es_automatico=False
        )

        logger.info(f"Cotizacion #{cotizacion_id} transicionada exitosamente a {nuevo_estado.value}")
        return cotizacion
