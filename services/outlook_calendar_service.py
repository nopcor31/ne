"""
Servicio para sincronizacion de agenda con Outlook Calendar mediante COM.
"""

import sys
from datetime import datetime, date, time
from typing import Optional
from loguru import logger
from core.exceptions import IntegracionOutlookError


class OutlookCalendarService:
    """Servicio para la creacion y actualizacion de eventos en Outlook Calendar."""

    def __init__(self):
        self._outlook_disponible = sys.platform == "win32"

    def crear_evento_calendario(
        self,
        titulo: str,
        fecha: date,
        hora_inicio: time,
        hora_fin: time,
        ubicacion: str,
        descripcion: str
    ) -> Optional[str]:
        """
        Crea una cita/evento en el calendario por defecto de Outlook.
        
        Returns:
            Optional[str]: EntryID del evento creado en Outlook para referencias futuras.
        """
        if not self._outlook_disponible:
            logger.warning("Integracion COM con Outlook no disponible. Evento simulado.")
            return "MOCK_OUTLOOK_ENTRY_ID_123"

        try:
            import win32com.client
            outlook_app = win32com.client.Dispatch("Outlook.Application")
            appointment = outlook_app.CreateItem(1)  # 1 = olAppointmentItem

            inicio_dt = datetime.combine(fecha, hora_inicio)
            fin_dt = datetime.combine(fecha, hora_fin)
            duracion_minutos = int((fin_dt - inicio_dt).total_seconds() / 60)

            appointment.Subject = titulo
            appointment.Start = inicio_dt.strftime("%Y-%m-%d %H:%M")
            appointment.Duration = duracion_minutos
            appointment.Location = ubicacion
            appointment.Body = descripcion
            appointment.ReminderSet = True
            appointment.ReminderMinutesBeforeStart = 60

            appointment.Save()
            entry_id = appointment.EntryID
            logger.info(f"Evento agendado en Outlook Calendar [EntryID: {entry_id}]: {titulo}")
            return entry_id

        except Exception as exc:
            logger.error(f"Error al agendar evento en Outlook Calendar: {exc}")
            raise IntegracionOutlookError(str(exc))
