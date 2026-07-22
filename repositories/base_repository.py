"""
Repositorio base generico para acceso a datos desacoplado.

Proporciona operaciones CRUD estandarizadas, busquedas, filtros y paginacion
sobre cualquier modelo SQLAlchemy en Python 3.13 / SQLAlchemy 2.x.
"""

from typing import Generic, TypeVar, Type, List, Optional, Any, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func, desc, asc
from core.database import Base
from core.exceptions import EntidadNoEncontradaError

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Clase base de repositorio con operaciones CRUD, filtros, busquedas y paginacion.
    
    Attributes:
        model (Type[ModelType]): Clase del modelo SQLAlchemy gestionado.
        session (Session): Sesion activa de SQLAlchemy.
    """

    def __init__(self, model: Type[ModelType], db_session: Session):
        """
        Inicializa el repositorio con el modelo y la sesion de BD.
        
        Args:
            model (Type[ModelType]): Modelo SQLAlchemy.
            db_session (Session): Sesion activa de SQLAlchemy.
        """
        self.model = model
        self.session = db_session

    def get_by_id(self, id_entidad: int) -> Optional[ModelType]:
        """Obtiene un registro por su clave primaria."""
        stmt = select(self.model).where(self.model.id == id_entidad)
        return self.session.scalar(stmt)

    def get_by_id_or_fail(self, id_entidad: int) -> ModelType:
        """Obtiene un registro por su ID o lanza EntidadNoEncontradaError."""
        entidad = self.get_by_id(id_entidad)
        if not entidad:
            raise EntidadNoEncontradaError(self.model.__name__, id_entidad)
        return entidad

    def exists(self, id_entidad: int) -> bool:
        """Verifica si existe un registro con el ID especificado."""
        stmt = select(func.count(self.model.id)).where(self.model.id == id_entidad)
        count = self.session.scalar(stmt) or 0
        return count > 0

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """Obtiene todos los registros con paginacion basica."""
        stmt = select(self.model).offset(skip).limit(limit)
        return list(self.session.scalars(stmt).all())

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Calcula el total de registros que coinciden opcionalmente con un diccionario de filtros.
        """
        stmt = select(func.count()).select_from(self.model)
        if filters:
            for campo, valor in filters.items():
                if hasattr(self.model, campo) and valor is not None:
                    stmt = stmt.where(getattr(self.model, campo) == valor)
        return self.session.scalar(stmt) or 0

    def find_filtered(
        self,
        filters: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        descending: bool = False
    ) -> List[ModelType]:
        """
        Busca registros aplicando un diccionario de filtros dinamicos y ordenacion.
        """
        stmt = select(self.model)
        if filters:
            for campo, valor in filters.items():
                if hasattr(self.model, campo) and valor is not None:
                    stmt = stmt.where(getattr(self.model, campo) == valor)

        if order_by and hasattr(self.model, order_by):
            columna = getattr(self.model, order_by)
            stmt = stmt.order_by(desc(columna) if descending else asc(columna))

        stmt = stmt.offset(skip).limit(limit)
        return list(self.session.scalars(stmt).all())

    def get_paginated(
        self,
        page: int = 1,
        page_size: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        descending: bool = False
    ) -> Dict[str, Any]:
        """
        Obtiene una pagina de registros formateada con metadatos de paginacion.
        
        Returns:
            Dict con keys: items, total, page, page_size, total_pages
        """
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20

        total = self.count(filters)
        skip = (page - 1) * page_size
        items = self.find_filtered(
            filters=filters,
            skip=skip,
            limit=page_size,
            order_by=order_by,
            descending=descending
        )

        total_pages = (total + page_size - 1) // page_size if total > 0 else 1

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages
        }

    def create(self, entidad: ModelType) -> ModelType:
        """Agrega un nuevo registro a la sesion y persiste."""
        self.session.add(entidad)
        self.session.flush()
        return entidad

    def bulk_create(self, entidades: List[ModelType]) -> List[ModelType]:
        """Inserta multiples registros en la base de datos."""
        self.session.add_all(entidades)
        self.session.flush()
        return entidades

    def update(self, id_entidad: int, valores: Dict[str, Any]) -> ModelType:
        """Actualiza atributos de un registro existente."""
        entidad = self.get_by_id_or_fail(id_entidad)
        for clave, valor in valores.items():
            if hasattr(entidad, clave):
                setattr(entidad, clave, valor)
        self.session.flush()
        return entidad

    def delete(self, id_entidad: int) -> bool:
        """Elimina un registro de la base de datos por su ID."""
        entidad = self.get_by_id(id_entidad)
        if entidad:
            self.session.delete(entidad)
            self.session.flush()
            return True
        return False
