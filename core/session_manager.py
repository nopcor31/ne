"""
Manejador de sesiones Singleton para SQLAlchemy.

Garantiza un unico punto de acceso thread-safe para la gestion de sesiones
SQLAlchemy en la aplicacion de escritorio PySide6.
"""

import threading
from typing import Generator
from contextlib import contextmanager
from sqlalchemy.orm import Session
from core.database import SessionLocal
from loguru import logger


class SessionManager:
    """
    Patron Singleton para la administracion centralizada de sesiones SQLAlchemy.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                logger.info("SessionManager Singleton instanciado correctamente.")
            return cls._instance

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Proporciona un contexto transaccional seguro para operaciones con la BD.
        
        Realiza commit automatico al salir del bloque sin errores o rollback
        si ocurre una excepcion.
        """
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as exc:
            session.rollback()
            logger.error(f"Error en transaccion de base de datos. Rollback ejecutado: {exc}")
            raise
        finally:
            session.close()

    def obtener_sesion(self) -> Session:
        """
        Crea y retorna una nueva sesion de SQLAlchemy.
        El llamador es responsable de cerrar la sesion.
        """
        return SessionLocal()


# Instancia singleton accesible globalmente
session_manager = SessionManager()
