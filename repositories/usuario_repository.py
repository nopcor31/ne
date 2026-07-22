"""
Repositorio especializado para la entidad Usuario.
"""

from typing import List, Optional
from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from models.usuario import Usuario
from core.enums import RolUsuario
from repositories.base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):
    """Repositorio de acceso a datos para usuarios del sistema."""

    def __init__(self, db_session: Session):
        super().__init__(Usuario, db_session)

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario activo o inactivo por su correo electronico."""
        stmt = select(Usuario).where(Usuario.email == email)
        return self.session.scalar(stmt)

    def buscar_por_documento(self, documento: str) -> Optional[Usuario]:
        """Busca un usuario por su numero de documento de identidad."""
        stmt = select(Usuario).where(Usuario.documento == documento)
        return self.session.scalar(stmt)

    def obtener_activos(self) -> List[Usuario]:
        """Obtiene la lista de todos los usuarios activos ordenados por nombre."""
        stmt = select(Usuario).where(Usuario.activo.is_(True)).order_by(Usuario.nombre_completo)
        return list(self.session.scalars(stmt).all())

    def obtener_por_rol(self, rol: RolUsuario) -> List[Usuario]:
        """Obtiene todos los usuarios activos asignados a un rol especifico."""
        stmt = (
            select(Usuario)
            .where(
                Usuario.rol == rol,
                Usuario.activo.is_(True)
            )
            .order_by(Usuario.nombre_completo)
        )
        return list(self.session.scalars(stmt).all())

    def buscar_por_texto(self, texto: str) -> List[Usuario]:
        """Busca usuarios por nombre, email o documento."""
        patron = f"%{texto}%"
        stmt = select(Usuario).where(
            or_(
                Usuario.nombre_completo.ilike(patron),
                Usuario.email.ilike(patron),
                Usuario.documento.ilike(patron)
            )
        )
        return list(self.session.scalars(stmt).all())
