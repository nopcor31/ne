"""
Repositorio especializado para la entidad Servicio.
"""

from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from models.servicio import Servicio
from repositories.base_repository import BaseRepository


class ServicioRepository(BaseRepository[Servicio]):
    """Repositorio de acceso a datos para catalogo de servicios medicos."""

    def __init__(self, db_session: Session):
        super().__init__(Servicio, db_session)

    def obtener_activos(self) -> List[Servicio]:
        """Obtiene todos los servicios medicos activos ordenados por nombre."""
        stmt = select(Servicio).where(Servicio.activo.is_(True)).order_by(Servicio.nombre)
        return list(self.session.scalars(stmt).all())

    def buscar_por_codigo(self, codigo: str) -> Optional[Servicio]:
        """Busca un servicio por su codigo unico identificador."""
        stmt = select(Servicio).where(Servicio.codigo == codigo)
        return self.session.scalar(stmt)

    def buscar_por_categoria(self, categoria: str) -> List[Servicio]:
        """Obtiene servicios pertenecientes a una categoria especifica."""
        stmt = (
            select(Servicio)
            .where(
                Servicio.categoria == categoria,
                Servicio.activo.is_(True)
            )
            .order_by(Servicio.nombre)
        )
        return list(self.session.scalars(stmt).all())

    def buscar_por_texto(self, texto: str) -> List[Servicio]:
        """Busca servicios por coincidencia en codigo, nombre o descripcion."""
        patron = f"%{texto}%"
        stmt = select(Servicio).where(
            or_(
                Servicio.codigo.ilike(patron),
                Servicio.nombre.ilike(patron),
                Servicio.descripcion.ilike(patron)
            )
        )
        return list(self.session.scalars(stmt).all())
