"""
Servicio para la programacion y agendamiento operativo de servicios.
"""

from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from models.programacion import Programacion
from repositories.programacion_repository import ProgramacionRepository
from repositories.evento_repository import EventoRepository
from services.outlook_calendar_service import OutlookCalendarService
from services.estado_service import EstadoService
from core.enums import EstadoProgramacion, EstadoCotizacion


class ProgramacionService:
    """Servicio para la programacion operativa de eventos aprobados."""

    def __init__(self, session: Session):
        self.session = session
        self.prog_repo = ProgramacionRepository(session)
        self.evento_repo = EventoRepository(session)
        self.calendar_service = OutlookCalendarService()
        self.estado_service = EstadoService(session)

    def programar_evento(
        self,
        cotizacion_id: int,
        evento_id: int,
        fecha_programada: date,
        recurso_asignado: str,
        usuario_id: int,
        notas: Optional[str] = None
    ) -> Programacion:
        """Agenda un evento en el calendario operativo y sincroniza con Outlook."""
        evento = self.evento_repo.get_by_id_or_fail(evento_id)

        # 1. Agendar en Outlook Calendar via COM
        titulo_evento = f"Servicio NE: {evento.servicio.nombre} — Cot #{cotizacion_id}"
        entry_id = self.calendar_service.crear_evento_calendario(
            titulo=titulo_evento,
            fecha=fecha_programada,
            hora_inicio=evento.hora_inicio,
            hora_fin=evento.hora_fin,
            ubicacion=evento.direccion,
            descripcion=f"Recurso Asignado: {recurso_asignado}\nNotas: {notas or 'N/A'}"
        )

        # 2. Guardar en base de datos
        prog = Programacion(
            cotizacion_id=cotizacion_id,
            evento_id=evento_id,
            fecha_programada=fecha_programada,
            hora_inicio=evento.hora_inicio,
            hora_fin=evento.hora_fin,
            recurso_asignado=recurso_asignado,
            notas=notas,
            outlook_event_id=entry_id,
            estado=EstadoProgramacion.CONFIRMADA
        )
        self.prog_repo.create(prog)
        self.session.flush()

        # 3. Transicionar estado de la cotizacion
        self.estado_service.transicionar(cotizacion_id, EstadoCotizacion.PROGRAMADA, usuario_id)

        return prog

    def obtener_programacion_rango(self, fecha_inicio: date, fecha_fin: date) -> List[Programacion]:
        """Obtiene la agenda operativa para un rango de fechas."""
        return self.prog_repo.obtener_por_rango_fechas(fecha_inicio, fecha_fin)
