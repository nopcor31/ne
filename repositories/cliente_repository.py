"""
Repositorio especializado para la entidad Cliente.
"""

from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from models.cliente import Cliente
from repositories.base_repository import BaseRepository


class ClienteRepository(BaseRepository[Cliente]):
    """Repositorio de acceso a datos para clientes."""

    def __init__(self, db_session: Session):
        super().__init__(Cliente, db_session)

    def buscar_por_nit(self, nit: str) -> Optional[Cliente]:
        """Busca un cliente por su NIT."""
        stmt = select(Cliente).where(Cliente.nit == nit)
        return self.session.scalar(stmt)

    def buscar_por_texto(self, texto: str) -> List[Cliente]:
        """Busca clientes por coincidencia en empresa o NIT."""
        patron = f"%{texto}%"
        stmt = select(Cliente).where(
            or_(
                Cliente.empresa.ilike(patron),
                Cliente.nit.ilike(patron),
                Cliente.correo_principal.ilike(patron)
            )
        )
        return list(self.session.scalars(stmt).all())

    def obtener_activos(self) -> List[Cliente]:
        """Obtiene la lista de clientes activos."""
        stmt = select(Cliente).where(Cliente.activo.is_(True)).order_by(Cliente.empresa)
        return list(self.session.scalars(stmt).all())
