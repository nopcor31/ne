"""
Servicio del motor de tarifas con patron Strategy y fallback automatico.
"""

from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from models.cliente import Cliente
from models.tarifa import Tarifa
from repositories.tarifa_repository import TarifaRepository
from repositories.cliente_repository import ClienteRepository
from core.enums import TipoCliente, TipoDia, TipoHorario
from core.exceptions import TarifaNoEncontradaError


class TarifaService:
    """Motor de evaluacion de tarifas con fallback a tarifa general."""

    def __init__(self, session: Session):
        self.session = session
        self.tarifa_repo = TarifaRepository(session)
        self.cliente_repo = ClienteRepository(session)

    def obtener_tarifa_aplicable(
        self,
        cliente_id: int,
        ciudad_id: int,
        servicio_id: int,
        tipo_dia: TipoDia,
        tipo_horario: TipoHorario,
        fecha_evaluacion: date
    ) -> Tarifa:
        """
        Obtiene la tarifa aplicable ejecutando la estrategia de busqueda:
        
        1. Si el cliente es de tipo ESPECIAL, busca primero una tarifa personalizada.
        2. Si no existe o el cliente es NORMAL, realiza fallback a la tarifa general (cliente_id = None).
        3. Si tampoco existe tarifa general, lanza TarifaNoEncontradaError.
        """
        cliente = self.cliente_repo.get_by_id_or_fail(cliente_id)

        # 1. Estrategia Cliente Especial
        if cliente.tipo_cliente == TipoCliente.ESPECIAL:
            tarifa_especial = self.tarifa_repo.buscar_tarifa_vigente(
                ciudad_id=ciudad_id,
                servicio_id=servicio_id,
                tipo_dia=tipo_dia,
                tipo_horario=tipo_horario,
                fecha_evaluacion=fecha_evaluacion,
                cliente_id=cliente.id
            )
            if tarifa_especial:
                return tarifa_especial

        # 2. Fallback a Tarifa General
        tarifa_general = self.tarifa_repo.buscar_tarifa_vigente(
            ciudad_id=ciudad_id,
            servicio_id=servicio_id,
            tipo_dia=tipo_dia,
            tipo_horario=tipo_horario,
            fecha_evaluacion=fecha_evaluacion,
            cliente_id=None
        )
        if tarifa_general:
            return tarifa_general

        # 3. Excepcion si no se encuentra ninguna tarifa
        raise TarifaNoEncontradaError(
            ciudad=f"ID {ciudad_id}",
            servicio=f"ID {servicio_id}",
            tipo_dia=tipo_dia.value,
            tipo_horario=tipo_horario.value
        )
