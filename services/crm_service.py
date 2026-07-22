"""
Servicio CRM para la gestion de interacciones y tareas por cliente.
"""

from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models.interaccion_crm import InteraccionCRM
from models.tarea import Tarea
from repositories.interaccion_repository import InteraccionRepository
from repositories.tarea_repository import TareaRepository
from core.enums import TipoInteraccionCRM, PrioridadTarea


class CRMService:
    """Servicio para administrar el historial de relacionamiento y tareas CRM."""

    def __init__(self, session: Session):
        self.session = session
        self.interaccion_repo = InteraccionRepository(session)
        self.tarea_repo = TareaRepository(session)

    def registrar_interaccion(
        self,
        cliente_id: int,
        tipo: TipoInteraccionCRM,
        asunto: str,
        usuario_id: int,
        descripcion: Optional[str] = None,
        cotizacion_id: Optional[int] = None
    ) -> InteraccionCRM:
        """Registra un nuevo punto de contacto con el cliente en el CRM."""
        interaccion = InteraccionCRM(
            cliente_id=cliente_id,
            cotizacion_id=cotizacion_id,
            tipo=tipo,
            asunto=asunto,
            descripcion=descripcion,
            usuario_id=usuario_id,
            fecha_hora=datetime.now()
        )
        return self.interaccion_repo.create(interaccion)

    def crear_tarea(
        self,
        titulo: str,
        fecha_vencimiento: datetime,
        usuario_asignado_id: int,
        usuario_creador_id: int,
        prioridad: PrioridadTarea = PrioridadTarea.MEDIA,
        descripcion: Optional[str] = None,
        cliente_id: Optional[int] = None,
        cotizacion_id: Optional[int] = None
    ) -> Tarea:
        """Crea una nueva tarea o recordatorio de seguimiento."""
        tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            prioridad=prioridad,
            fecha_vencimiento=fecha_vencimiento,
            usuario_asignado_id=usuario_asignado_id,
            usuario_creador_id=usuario_creador_id,
            cliente_id=cliente_id,
            cotizacion_id=cotizacion_id,
            completada=False
        )
        return self.tarea_repo.create(tarea)

    def marcar_tarea_completada(self, tarea_id: int) -> Tarea:
        """Marca una tarea como completada registrando la fecha de finalizacion."""
        tarea = self.tarea_repo.get_by_id_or_fail(tarea_id)
        tarea.completada = True
        tarea.fecha_completada = datetime.now()
        self.session.flush()
        return tarea

    def obtener_interacciones_cliente(self, cliente_id: int) -> List[InteraccionCRM]:
        """Obtiene la lista cronologica de interacciones de un cliente."""
        return self.interaccion_repo.obtener_por_cliente(cliente_id)

    def obtener_tareas_pendientes_usuario(self, usuario_id: int) -> List[Tarea]:
        """Obtiene las tareas pendientes asignadas a un usuario."""
        return self.tarea_repo.obtener_pendientes_por_usuario(usuario_id)
