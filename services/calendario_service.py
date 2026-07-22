"""
Servicio para reglas de calendario y calculo de franjas horarias.

Calcula horas diurnas/nocturnas y clasificacion de dias (ordinario vs festivo).
"""

from datetime import date, time, datetime, timedelta
from typing import Tuple, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.festivo import Festivo
from core.enums import TipoDia
from config.settings import settings


class CalendarioService:
    """Servicio con las reglas de negocio para franjas horarias y dias festivos."""

    def __init__(self, session: Session):
        self.session = session

    def determinar_tipo_dia(self, fecha_evaluar: date) -> TipoDia:
        """
        Determina si una fecha dada es un dia ORDINARIO o FESTIVO.
        
        Regla:
        - Si es Domingo (weekday == 6), es FESTIVO.
        - Si la fecha esta registrada en la tabla de festivos, es FESTIVO.
        - En otro caso, es ORDINARIO.
        """
        if fecha_evaluar.weekday() == 6:
            return TipoDia.FESTIVO

        stmt = select(Festivo).where(Festivo.fecha == fecha_evaluar)
        es_festivo = self.session.scalar(stmt) is not None
        if es_festivo:
            return TipoDia.FESTIVO

        return TipoDia.ORDINARIO

    def calcular_horas_diurnas_nocturnas(
        self,
        fecha_evaluar: date,
        hora_inicio: time,
        hora_fin: time
    ) -> Tuple[float, float]:
        """
        Calcula la cantidad exacta de horas diurnas y nocturnas trabajadas.
        
        Reglas:
        - DIURNO = 07:00 a 18:59:59 (07:00 - 19:00)
        - NOCTURNO = 19:00 a 06:59:59 (19:00 - 07:00)
        - Maneja automaticamente turnos que cruzan la medianoche.
        
        Returns:
            Tuple[float, float]: (horas_diurnas, horas_nocturnas)
        """
        inicio_dt = datetime.combine(fecha_evaluar, hora_inicio)
        fin_dt = datetime.combine(fecha_evaluar, hora_fin)

        if fin_dt <= inicio_dt:
            # El evento cruza la medianoche (ej. 20:00 a 04:00 del dia siguiente)
            fin_dt += timedelta(days=1)

        horas_diurnas = 0.0
        horas_nocturnas = 0.0
        cursor = inicio_dt

        frontera_diurna = time(settings.HORA_INICIO_DIURNO, 0)   # 07:00
        frontera_nocturna = time(settings.HORA_FIN_DIURNO, 0)   # 19:00

        while cursor < fin_dt:
            siguiente_corte = self._obtener_siguiente_corte(cursor, frontera_diurna, frontera_nocturna)
            tramo_fin = min(fin_dt, siguiente_corte)
            duracion_horas = (tramo_fin - cursor).total_seconds() / 3600.0

            if self._es_horario_diurno(cursor, frontera_diurna, frontera_nocturna):
                horas_diurnas += duracion_horas
            else:
                horas_nocturnas += duracion_horas

            cursor = tramo_fin

        return round(horas_diurnas, 2), round(horas_nocturnas, 2)

    def _es_horario_diurno(self, dt: datetime, inicio_diurno: time, inicio_nocturno: time) -> bool:
        """Verifica si un timestamp cae en la franja diurna [07:00, 19:00)."""
        t = dt.time()
        return inicio_diurno <= t < inicio_nocturno

    def _obtener_siguiente_corte(self, dt: datetime, inicio_diurno: time, inicio_nocturno: time) -> datetime:
        """Determina el proximo punto de cambio de franja horaria (07:00 o 19:00)."""
        fecha_actual = dt.date()
        corte_diurno = datetime.combine(fecha_actual, inicio_diurno)
        corte_nocturno = datetime.combine(fecha_actual, inicio_nocturno)
        corte_diurno_siguiente = datetime.combine(fecha_actual + timedelta(days=1), inicio_diurno)

        if dt < corte_diurno:
            return corte_diurno
        elif dt < corte_nocturno:
            return corte_nocturno
        else:
            return corte_diurno_siguiente
