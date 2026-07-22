"""
Servicio para la administracion de aprobaciones de Area Medica.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models.envio_area_medica import EnvioAreaMedica
from repositories.area_medica_repository import AreaMedicaRepository
from repositories.envio_area_medica_repository import EnvioAreaMedicaRepository
from services.estado_service import EstadoService
from core.enums import EstadoCotizacion


class AreaMedicaService:
    """Servicio para el flujo de aprobacion con el area medica."""

    def __init__(self, session: Session):
        self.session = session
        self.area_repo = AreaMedicaRepository(session)
        self.envio_repo = EnvioAreaMedicaRepository(session)
        self.estado_service = EstadoService(session)

    def enviar_a_area_medica(
        self, cotizacion_id: int, area_medica_id: int, usuario_id: int
    ) -> EnvioAreaMedica:
        """Envia un expediente de cotizacion a un area medica para revision tecnica."""
        envio = EnvioAreaMedica(
            cotizacion_id=cotizacion_id,
            area_medica_id=area_medica_id,
            usuario_envio_id=usuario_id,
            fecha_envio=datetime.now(),
            aprobado=None
        )
        self.envio_repo.create(envio)
        self.session.flush()

        # Transicionar estado de cotizacion
        self.estado_service.transicionar(
            cotizacion_id, EstadoCotizacion.PENDIENTE_AREA_MEDICA, usuario_id
        )
        return envio

    def registrar_respuesta_area_medica(
        self,
        envio_id: int,
        aprobado: bool,
        usuario_id: int,
        observaciones: Optional[str] = None
    ) -> EnvioAreaMedica:
        """Registra el concepto tecnico emitido por el area medica."""
        envio = self.envio_repo.get_by_id_or_fail(envio_id)
        envio.aprobado = aprobado
        envio.fecha_respuesta = datetime.now()
        envio.observaciones_respuesta = observaciones
        self.session.flush()

        # Transicionar estado segun aprobacion
        nuevo_estado = (
            EstadoCotizacion.APROBADA_AREA_MEDICA if aprobado else EstadoCotizacion.RECHAZADA_CLIENTE
        )
        self.estado_service.transicionar(
            envio.cotizacion_id, nuevo_estado, usuario_id, observacion=observaciones
        )
        return envio
