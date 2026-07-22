"""
Repositorio especializado para la entidad ContactoCliente.
"""

from typing import List, Optional
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from models.contacto_cliente import ContactoCliente
from repositories.base_repository import BaseRepository


class ContactoRepository(BaseRepository[ContactoCliente]):
    """Repositorio de acceso a datos para contactos de clientes."""

    def __init__(self, db_session: Session):
        super().__init__(ContactoCliente, db_session)

    def obtener_por_cliente(self, cliente_id: int) -> List[ContactoCliente]:
        """Obtiene todos los contactos activos de un cliente."""
        stmt = select(ContactoCliente).where(
            ContactoCliente.cliente_id == cliente_id,
            ContactoCliente.activo.is_(True)
        )
        return list(self.session.scalars(stmt).all())

    def obtener_principal(self, cliente_id: int) -> Optional[ContactoCliente]:
        """Obtiene el contacto principal de un cliente."""
        stmt = select(ContactoCliente).where(
            ContactoCliente.cliente_id == cliente_id,
            ContactoCliente.es_principal.is_(True),
            ContactoCliente.activo.is_(True)
        )
        return self.session.scalar(stmt)

    def establecer_principal(self, cliente_id: int, contacto_id: int) -> None:
        """Marca un contacto como principal y desmarca los demás del cliente."""
        # Desmarcar todos los contactos del cliente
        self.session.execute(
            update(ContactoCliente)
            .where(ContactoCliente.cliente_id == cliente_id)
            .values(es_principal=False)
        )
        # Marcar el seleccionado
        self.session.execute(
            update(ContactoCliente)
            .where(ContactoCliente.id == contacto_id)
            .values(es_principal=True)
        )
        self.session.flush()
