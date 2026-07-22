"""
Servicio del motor de evaluacion y generacion de Alertas proactivas.
"""

from typing import List
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from models.alerta import Alerta
from repositories.alerta_repository import AlertaRepository
from repositories.cotizacion_repository import CotizacionRepository
from repositories.factura_repository import FacturaRepository
from repositories.tarea_repository import TareaRepository
from core.enums import TipoAlerta, PrioridadAlerta, EstadoCotizacion
from config.settings import settings
from loguru import logger


class AlertaService:
    """Motor de evaluacion periodica de condiciones de alerta."""

    def __init__(self, session: Session):
        self.session = session
        self.alerta_repo = AlertaRepository(session)
        self.cotizacion_repo = CotizacionRepository(session)
        self.factura_repo = FacturaRepository(session)
        self.tarea_repo = TareaRepository(session)

    def evaluar_y_generar_alertas(self, usuario_id: int) -> List[Alerta]:
        """
        Ejecuta todas las reglas de evaluacion y genera nuevas alertas activas.
        
        Returns:
            List[Alerta]: Lista de alertas generadas en este ciclo.
        """
        alertas_generadas = []
        ahora = datetime.now()
        hoy = date.today()

        # Regla 1: Cotizacion sin respuesta
        limite_cotiz = ahora - timedelta(days=settings.DIAS_COTIZACION_SIN_RESPUESTA)
        cotizaciones_enviadas = self.cotizacion_repo.obtener_por_estado(EstadoCotizacion.ENVIADA_CLIENTE)
        for cot in cotizaciones_enviadas:
            if cot.fecha_enviada_cliente and cot.fecha_enviada_cliente < limite_cotiz:
                alert = self._crear_alerta_si_no_existe(
                    tipo=TipoAlerta.COTIZACION_SIN_RESPUESTA,
                    titulo=f"Cotización sin respuesta: {cot.numero_cotizacion}",
                    mensaje=f"La cotización para {cot.cliente.empresa} lleva más de {settings.DIAS_COTIZACION_SIN_RESPUESTA} días sin respuesta.",
                    entidad_tipo="cotizacion",
                    entidad_id=cot.id,
                    prioridad=PrioridadAlerta.ADVERTENCIA,
                    usuario_id=usuario_id
                )
                if alert:
                    alertas_generadas.append(alert)

        # Regla 2: Facturas vencidas no pagadas
        facturas_vencidas = self.factura_repo.obtener_vencidas(hoy)
        for fac in facturas_vencidas:
            alert = self._crear_alerta_si_no_existe(
                tipo=TipoAlerta.PAGO_PENDIENTE,
                titulo=f"Factura Vencida: {fac.numero_factura}",
                mensaje=f"La factura {fac.numero_factura} venció el {fac.fecha_vencimiento} y se encuentra pendiente de pago.",
                entidad_tipo="factura",
                entidad_id=fac.id,
                prioridad=PrioridadAlerta.CRITICA,
                usuario_id=usuario_id
            )
            if alert:
                alertas_generadas.append(alert)

        # Regla 3: Tareas vencidas
        tareas_vencidas = self.tarea_repo.obtener_vencidas(ahora)
        for tar in tareas_vencidas:
            alert = self._crear_alerta_si_no_existe(
                tipo=TipoAlerta.TAREA_VENCIDA,
                titulo=f"Tarea Vencida: {tar.titulo}",
                mensaje=f"La tarea '{tar.titulo}' venció el {tar.fecha_vencimiento}.",
                entidad_tipo="tarea",
                entidad_id=tar.id,
                prioridad=PrioridadAlerta.ADVERTENCIA,
                usuario_id=usuario_id
            )
            if alert:
                alertas_generadas.append(alert)

        if alertas_generadas:
            logger.info(f"Ciclo de alertas completado. {len(alertas_generadas)} nuevas alertas generadas.")

        return alertas_generadas

    def _crear_alerta_si_no_existe(
        self,
        tipo: TipoAlerta,
        titulo: str,
        mensaje: str,
        entidad_tipo: str,
        entidad_id: int,
        prioridad: PrioridadAlerta,
        usuario_id: int
    ) -> Alerta:
        """Crea una alerta asegurando que no exista un duplicado activo previo."""
        existente = self.alerta_repo.buscar_existente(tipo, entidad_tipo, entidad_id, usuario_id)
        if existente:
            return None

        alerta = Alerta(
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje,
            entidad_tipo=entidad_tipo,
            entidad_id=entidad_id,
            prioridad=prioridad,
            usuario_id=usuario_id,
            activa=True,
            fecha_creacion=datetime.now()
        )
        self.alerta_repo.create(alerta)
        self.session.flush()
        return alerta

    def obtener_alertas_activas(self, usuario_id: int) -> List[Alerta]:
        """Obtiene las alertas activas para el usuario."""
        return self.alerta_repo.obtener_activas_por_usuario(usuario_id)

    def descartar_alerta(self, alerta_id: int) -> None:
        """Marca una alerta como inactiva/descartada."""
        alerta = self.alerta_repo.get_by_id_or_fail(alerta_id)
        alerta.activa = False
        self.session.flush()
