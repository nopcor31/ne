"""
Utilidades de formateo de texto, moneda (COP), fechas y duraciones.
"""

from datetime import datetime, date, time
from typing import Union


def formatear_cop(valor: Union[float, int]) -> str:
    """Formatea un numero flotante o entero como moneda Pesos Colombianos (COP)."""
    if valor is None:
        return "$0"
    return f"${valor:,.0f}".replace(",", ".")


def formatear_fecha(fecha: Union[date, datetime]) -> str:
    """Formatea una fecha como 'DD/MM/AAAA'."""
    if not fecha:
        return ""
    return fecha.strftime("%d/%m/%Y")


def formatear_fecha_hora(fecha_hora: datetime) -> str:
    """Formatea un objeto datetime como 'DD/MM/AAAA HH:MM'."""
    if not fecha_hora:
        return ""
    return fecha_hora.strftime("%d/%m/%Y %H:%M")


def formatear_hora(hora: time) -> str:
    """Formatea un objeto time como 'HH:MM' (24h)."""
    if not hora:
        return ""
    return hora.strftime("%H:%M")
