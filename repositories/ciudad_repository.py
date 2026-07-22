"""
Repositorio especializado para la entidad Ciudad.
"""

from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from models.ciudad import Ciudad
from repositories.base_repository import BaseRepository


class CiudadRepository(BaseRepository[Ciudad]):
    """Repositorio de acceso a datos para ciudades de cobertura operativa."""

    def __init__(self, db_session: Session):
        super().__init__(Ciudad, db_session)

    def obtener_activas(self) -> List[Ciudad]:
        """Obtiene la lista de ciudades activas para operacion."""
        stmt = select(Ciudad).where(Ciudad.activo.is_(True)).order_by(Ciudad.nombre)
        return list(self.session.scalars(stmt).all())

    def buscar_por_nombre(self, nombre: str) -> Optional[Ciudad]:
        """Busca una ciudad por su nombre exacto o ignorando mayusculas/minusculas."""
        stmt = select(Ciudad).where(Ciudad.nombre.ilike(nombre))
        return self.session.scalar(stmt)

    def buscar_por_texto(self, texto: str) -> List[Ciudad]:
        """Busca ciudades por coincidencia en nombre o departamento."""
        patron = f"%{texto}%"
        stmt = select(Ciudad).where(
            or_(
                Ciudad.nombre.ilike(patron),
                Ciudad.departamento.ilike(patron),
                Ciudad.codigo_dane.ilike(patron)
            )
        )
        return list(self.session.scalars(stmt).all())
