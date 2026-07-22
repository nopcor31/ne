"""
Motor y base declarativa de la base de datos SQLAlchemy 2.x.

Configura la conexion SQLite con pragmas optimizados para integridad referencial,
journal_mode WAL y sesion sincrona.
"""

from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from config.settings import settings
from loguru import logger


# Engine SQLAlchemy 2.x para SQLite
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,  # Cambiar a True para depuracion SQL detallada
    future=True
)


@event.listens_for(engine, "connect")
def _habilitar_foreign_keys_sqlite(dbapi_connection, connection_record) -> None:
    """Activa el soporte de claves foraneas y WAL en SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.close()


# Fabrica de sesiones SQLAlchemy
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Clase base declarativa para todas las entidades ORM."""
    pass


def inicializar_base_datos() -> None:
    """
    Crea todas las tablas definidas en los modelos ORM si no existen.
    
    Asegura la creacion idempotente de la estructura de base de datos.
    """
    logger.info("Inicializando esquema de base de datos SQLite...")
    Base.metadata.create_all(bind=engine)
    logger.info("Esquema de base de datos verificado e inicializado correctamente.")


def get_db() -> Generator[Session, None, None]:
    """
    Generador dependiente para obtencion de sesion de base de datos con autoclose.
    
    Yields:
        Session: Sesion de SQLAlchemy.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
