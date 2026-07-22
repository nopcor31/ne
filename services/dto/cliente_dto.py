"""
Data Transfer Objects (DTO) para la entidad Cliente.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from core.enums import TipoCliente


@dataclass
class ContactoDTO:
    """DTO para transferencia de informacion de un contacto de cliente."""
    id: Optional[int]
    nombre: str
    cargo: Optional[str]
    correo: Optional[str]
    telefono: Optional[str]
    es_principal: bool


@dataclass
class ClienteDTO:
    """DTO para transferencia de informacion completa de un cliente."""
    id: Optional[int]
    empresa: str
    nit: str
    correo_principal: str
    telefono_principal: str
    tipo_cliente: TipoCliente
    sector: Optional[str]
    ciudad_id: int
    ciudad_nombre: Optional[str]
    direccion: Optional[str]
    sitio_web: Optional[str]
    observaciones: Optional[str]
    activo: bool
    fecha_creacion: Optional[datetime]
    contactos: Optional[List[ContactoDTO]] = None
