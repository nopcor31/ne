"""
Repositorio especializado para la entidad Configuracion.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.configuracion import Configuracion
from repositories.base_repository import BaseRepository


class ConfiguracionRepository(BaseRepository[Configuracion]):
    """Repositorio de acceso a datos para parametros de configuracion global del sistema."""

    def __init__(self, db_session: Session):
        super().__init__(Configuracion, db_session)

    def obtener_valor(self, clave: str, valor_defecto: Optional[str] = None) -> Optional[str]:
        """Obtiene el valor alfanumerico de una clave de configuracion."""
        stmt = select(Configuracion).where(Configuracion.clave == clave)
        config = self.session.scalar(stmt)
        if config:
            return config.valor
        return valor_defecto

    def obtener_por_clave(self, clave: str) -> Optional[Configuracion]:
        """Obtiene el objeto de configuracion completo por su clave primaria identitaria."""
        stmt = select(Configuracion).where(Configuracion.clave == clave)
        return self.session.scalar(stmt)

    def guardar_valor(self, clave: str, valor: str, descripcion: Optional[str] = None) -> Configuracion:
        """Crea o actualiza una variable de configuracion global."""
        config = self.obtener_por_clave(clave)
        if config:
            config.valor = valor
            if descripcion:
                config.descripcion = descripcion
        else:
            config = Configuracion(
                clave=clave,
                valor=valor,
                descripcion=descripcion or f"Parametro {clave}"
            )
            self.session.add(config)
        self.session.flush()
        return config
