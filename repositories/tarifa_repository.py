"""
Repositorio especializado para la entidad Tarifa.
"""

from datetime import date
from typing import Optional, List
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session
from models.tarifa import Tarifa
from core.enums import TipoDia, TipoHorario
from repositories.base_repository import BaseRepository


class TarifaRepository(BaseRepository[Tarifa]):
    """Repositorio de acceso a datos para las tarifas del motor de precios."""

    def __init__(self, db_session: Session):
        super().__init__(Tarifa, db_session)

    def buscar_tarifa_vigente(
        self,
        ciudad_id: int,
        servicio_id: int,
        tipo_dia: TipoDia,
        tipo_horario: TipoHorario,
        fecha_evaluacion: date,
        cliente_id: Optional[int] = None
    ) -> Optional[Tarifa]:
        """
        Busca la tarifa vigente para los parametros especificados.
        Soporta consulta por cliente especifico (cliente_id) o tarifa general (cliente_id = None).
        """
        condiciones = [
            Tarifa.ciudad_id == ciudad_id,
            Tarifa.servicio_id == servicio_id,
            Tarifa.tipo_dia == tipo_dia,
            Tarifa.tipo_horario == tipo_horario,
            Tarifa.activo.is_(True),
            Tarifa.vigente_desde <= fecha_evaluacion,
            or_(
                Tarifa.vigente_hasta.is_(None),
                Tarifa.vigente_hasta >= fecha_evaluacion
            )
        ]

        if cliente_id is not None:
            condiciones.append(Tarifa.cliente_id == cliente_id)
        else:
            condiciones.append(Tarifa.cliente_id.is_(None))

        stmt = select(Tarifa).where(and_(*condiciones)).order_by(Tarifa.vigente_desde.desc())
        return self.session.scalar(stmt)

    def obtener_tarifas_cliente(self, cliente_id: int) -> List[Tarifa]:
        """Obtiene todas las tarifas especiales configuradas para un cliente."""
        stmt = (
            select(Tarifa)
            .where(
                Tarifa.cliente_id == cliente_id,
                Tarifa.activo.is_(True)
            )
            .order_by(Tarifa.ciudad_id, Tarifa.servicio_id)
        )
        return list(self.session.scalars(stmt).all())
