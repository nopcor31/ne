"""
Controlador MVC para la gestion de Clientes con señales Qt.
"""

from typing import List, Optional
from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.cliente_service import ClienteService
from services.dto.cliente_dto import ClienteDTO, ContactoDTO


class ClienteController(QObject):
    """Controlador para orquestar la vista de clientes y sus contactos mediante señales Qt."""

    clientes_cargados = Signal(list)
    cliente_creado = Signal(object)
    cliente_actualizado = Signal(object)
    contacto_agregado = Signal(object)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot()
    def listar_clientes(self) -> List[ClienteDTO]:
        """Obtiene la lista de todos los clientes activos."""
        try:
            with session_manager.session_scope() as session:
                service = ClienteService(session)
                clientes = service.listar_clientes()
                dtos = [
                    ClienteDTO(
                        id=c.id,
                        empresa=c.empresa,
                        nit=c.nit,
                        correo_principal=c.correo_principal,
                        telefono_principal=c.telefono_principal,
                        tipo_cliente=c.tipo_cliente,
                        sector=c.sector,
                        ciudad_id=c.ciudad_id,
                        ciudad_nombre=c.ciudad.nombre if c.ciudad else None,
                        direccion=c.direccion,
                        sitio_web=c.sitio_web,
                        observaciones=c.observaciones,
                        activo=c.activo,
                        fecha_creacion=c.fecha_creacion
                    )
                    for c in clientes
                ]
                self.clientes_cargados.emit(dtos)
                return dtos
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def obtener_cliente(self, cliente_id: int) -> Optional[ClienteDTO]:
        """Obtiene los detalles de un cliente por su ID."""
        try:
            with session_manager.session_scope() as session:
                service = ClienteService(session)
                c = service.obtener_cliente(cliente_id)
                if not c:
                    return None
                return ClienteDTO(
                    id=c.id,
                    empresa=c.empresa,
                    nit=c.nit,
                    correo_principal=c.correo_principal,
                    telefono_principal=c.telefono_principal,
                    tipo_cliente=c.tipo_cliente,
                    sector=c.sector,
                    ciudad_id=c.ciudad_id,
                    ciudad_nombre=c.ciudad.nombre if c.ciudad else None,
                    direccion=c.direccion,
                    sitio_web=c.sitio_web,
                    observaciones=c.observaciones,
                    activo=c.activo,
                    fecha_creacion=c.fecha_creacion
                )
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(object, int)
    def crear_cliente(self, dto: ClienteDTO, usuario_id: int) -> int:
        """Crea un nuevo cliente y retorna su ID."""
        try:
            with session_manager.session_scope() as session:
                service = ClienteService(session)
                nuevo_cliente = service.crear_cliente(dto, usuario_id)
                self.cliente_creado.emit(nuevo_cliente)
                return nuevo_cliente.id
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, object, int)
    def actualizar_cliente(self, cliente_id: int, dto: ClienteDTO, usuario_id: int):
        """Actualiza la informacion de un cliente."""
        try:
            with session_manager.session_scope() as session:
                service = ClienteService(session)
                cliente_actualizado = service.actualizar_cliente(cliente_id, dto, usuario_id)
                self.cliente_actualizado.emit(cliente_actualizado)
                return cliente_actualizado
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(str)
    def buscar_clientes(self, texto: str) -> List[ClienteDTO]:
        """Busca clientes por coincidencia de texto."""
        try:
            with session_manager.session_scope() as session:
                service = ClienteService(session)
                clientes = service.buscar_clientes(texto)
                dtos = [
                    ClienteDTO(
                        id=c.id,
                        empresa=c.empresa,
                        nit=c.nit,
                        correo_principal=c.correo_principal,
                        telefono_principal=c.telefono_principal,
                        tipo_cliente=c.tipo_cliente,
                        sector=c.sector,
                        ciudad_id=c.ciudad_id,
                        ciudad_nombre=c.ciudad.nombre if c.ciudad else None,
                        direccion=c.direccion,
                        sitio_web=c.sitio_web,
                        observaciones=c.observaciones,
                        activo=c.activo,
                        fecha_creacion=c.fecha_creacion
                    )
                    for c in clientes
                ]
                self.clientes_cargados.emit(dtos)
                return dtos
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, object)
    def agregar_contacto(self, cliente_id: int, dto: ContactoDTO):
        """Agrega un contacto adicional a un cliente existente."""
        try:
            with session_manager.session_scope() as session:
                service = ClienteService(session)
                contacto = service.agregar_contacto(cliente_id, dto)
                self.contacto_agregado.emit(contacto)
                return contacto
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def listar_contactos(self, cliente_id: int):
        """Obtiene la lista de contactos asociados a un cliente."""
        try:
            with session_manager.session_scope() as session:
                service = ClienteService(session)
                return service.listar_contactos(cliente_id)
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
