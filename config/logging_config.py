"""
Modulo de configuracion del sistema de bitacoras (logging).

Configura Loguru con rotacion diaria de archivos de log, formato detallado,
retencion de logs y niveles por modulo para asegurar trazabilidad.
"""

import sys
from loguru import logger
from config.settings import settings


def configurar_logging() -> None:
    """
    Configura Loguru para el manejo centralizado de logs.
    
    Establece la salida a consola y a archivo de texto con rotacion diaria,
    compresion zip y formato estructurado.
    """
    # Eliminar manejadores por defecto de Loguru
    logger.remove()

    # Formato personalizado de logs
    formato_log = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )

    # 1. Salida a Consola (stdout)
    logger.add(
        sys.stdout,
        format=formato_log,
        level="INFO",
        colorize=True,
        enqueue=True
    )

    # 2. Salida a Archivo Diario Rotativo
    archivo_log = settings.LOGS_DIR / "crm_{time:YYYY-MM-DD}.log"
    logger.add(
        archivo_log,
        format=formato_log,
        level="DEBUG",
        rotation="00:00",         # Rotacion a la medianoche
        retention="30 days",       # Retener logs de los ultimos 30 dias
        compression="zip",        # Comprimir logs antiguos
        encoding="utf-8",
        enqueue=True,
        backtrace=True,
        diagnose=True
    )

    logger.info(f"Sistema de logging inicializado. Logs guardados en: {settings.LOGS_DIR}")
