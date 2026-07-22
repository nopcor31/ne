"""
Generador de numeros consecutivos para cotizaciones (COT-AAAA-NNNN).
"""

from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from models.cotizacion import Cotizacion


class NumeroGenerador:
    """Generador thread-safe de consecutivos de cotizaciones."""

    @staticmethod
    def generar_numero_cotizacion(session: Session) -> str:
        """
        Genera el siguiente numero consecutivo de cotizacion para el año actual.
        Ejemplo: COT-2026-0001, COT-2026-0002.
        """
        anio_actual = datetime.now().year
        prefijo = f"COT-{anio_actual}-"

        # Buscar la ultima cotización con el prefijo del año
        stmt = (
            select(func.max(Cotizacion.numero_cotizacion))
            .where(Cotizacion.numero_cotizacion.like(f"{prefijo}%"))
        )
        ultimo_numero = session.scalar(stmt)

        if not ultimo_numero:
            siguiente_consecutivo = 1
        else:
            try:
                consecutivo_str = ultimo_numero.split("-")[-1]
                siguiente_consecutivo = int(consecutivo_str) + 1
            except (ValueError, IndexError):
                siguiente_consecutivo = 1

        return f"{prefijo}{siguiente_consecutivo:04d}"
