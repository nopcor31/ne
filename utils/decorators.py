"""
Decoradores transversales para la aplicacion CRM.
"""

from functools import wraps
from typing import Callable, Any
from services.historial_service import HistorialService
from loguru import logger


def registrar_historial(accion_nombre: str, entidad_tipo: str):
    """
    Decorador para registrar automaticamente cambios de estado o acciones
    en la bitacora de auditoria (HistorialActividad).
    
    Args:
        accion_nombre (str): Nombre legible de la accion ejecutada.
        entidad_tipo (str): Tipo de entidad ("cotizacion", "cliente", etc.).
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            resultado = func(self, *args, **kwargs)
            try:
                # Se asume que self posee acceso a session y usuario_id
                session = getattr(self, "session", None)
                if session:
                    historial_svc = HistorialService(session)
                    usuario_id = kwargs.get("usuario_id") or getattr(self, "usuario_id", 1)
                    entidad_id = getattr(resultado, "id", None) or kwargs.get("cotizacion_id", 0)

                    historial_svc.registrar_accion(
                        usuario_id=usuario_id,
                        entidad_tipo=entidad_tipo,
                        entidad_id=entidad_id,
                        accion=accion_nombre,
                        detalle=f"Accion '{func.__name__}' ejecutada exitosamente",
                        es_automatico=True
                    )
            except Exception as exc:
                logger.error(f"Error en decorador @registrar_historial: {exc}")

            return resultado
        return wrapper
    return decorator
