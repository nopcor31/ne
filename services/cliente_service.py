"""
Servicio para la gestion de Clientes y sus Contactos.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from models.cliente import Cliente
from models.contacto_cliente import ContactoCliente
from repositories.cliente_repository import ClienteRepository
from repositories.contacto_repository import ContactoRepository
from services.dto.cliente_dto import ClienteDTO, ContactoDTO
from core.exceptions import ValidacionError


class ClienteService:
    """Servicio de negocio para la administracion de clientes y contactos."""

    def __init__(self, session: Session):
        self.session = session
        self.cliente_repo = ClienteRepository(session)
        self.contacto_repo = ContactoRepository(session)

    def crear_cliente(self, dto: ClienteDTO, usuario_id: int) -> Cliente:
        """Crea un nuevo cliente verificando que el NIT no este duplicado."""
        existente = self.cliente_repo.buscar_por_nit(dto.nit)
        if existente:
            raise ValidacionError(f"Ya existe un cliente registrado con el NIT {dto.nit}.")

        cliente = Cliente(
            empresa=dto.empresa,
            nit=dto.nit,
            correo_principal=dto.correo_principal,
            telefono_principal=dto.telefono_principal,
            tipo_cliente=dto.tipo_cliente,
            sector=dto.sector,
            ciudad_id=dto.ciudad_id,
            direccion=dto.direccion,
            sitio_web=dto.sitio_web,
            observaciones=dto.observaciones,
            activo=True,
            usuario_creador_id=usuario_id
        )
        self.cliente_repo.create(cliente)

        # Crear contacto principal inicial si se proporciona
        if dto.contactos:
            for c_dto in dto.contactos:
                contacto = ContactoCliente(
                    cliente_id=cliente.id,
                    nombre=c_dto.nombre,
                    cargo=c_dto.cargo,
                    correo=c_dto.correo,
                    telefono=c_dto.telefono,
                    es_principal=c_dto.es_principal,
                    activo=True
                )
                self.contacto_repo.create(contacto)

        self.session.flush()
        return cliente

    def actualizar_cliente(self, cliente_id: int, dto: ClienteDTO) -> Cliente:
        """Actualiza los datos basicos de un cliente existente."""
        cliente = self.cliente_repo.get_by_id_or_fail(cliente_id)

        valores_actualizar = {
            "empresa": dto.empresa,
            "correo_principal": dto.correo_principal,
            "telefono_principal": dto.telefono_principal,
            "tipo_cliente": dto.tipo_cliente,
            "sector": dto.sector,
            "ciudad_id": dto.ciudad_id,
            "direccion": dto.direccion,
            "sitio_web": dto.sitio_web,
            "observaciones": dto.observaciones,
            "activo": dto.activo
        }
        return self.cliente_repo.update(cliente_id, valores_actualizar)

    def agregar_contacto(self, cliente_id: int, contacto_dto: ContactoDTO) -> ContactoCliente:
        """Agrega un nuevo contacto a un cliente existente."""
        self.cliente_repo.get_by_id_or_fail(cliente_id)

        contacto = ContactoCliente(
            cliente_id=cliente_id,
            nombre=contacto_dto.nombre,
            cargo=contacto_dto.cargo,
            correo=contacto_dto.correo,
            telefono=contacto_dto.telefono,
            es_principal=contacto_dto.es_principal,
            activo=True
        )
        self.contacto_repo.create(contacto)

        if contacto_dto.es_principal:
            self.contacto_repo.establecer_principal(cliente_id, contacto.id)

        return contacto

    def listar_clientes(self) -> List[Cliente]:
        """Obtiene la lista de clientes activos."""
        return self.cliente_repo.obtener_activos()

    def buscar_clientes(self, texto: str) -> List[Cliente]:
        """Busca clientes por coincidencia de texto en NIT o Nombre de Empresa."""
        return self.cliente_repo.buscar_por_texto(texto)
