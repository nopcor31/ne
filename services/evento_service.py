"""
Servicio para el calculo automatico y gestion de eventos de servicio.
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models.evento import Evento
from models.extra_evento import ExtraEvento
from repositories.evento_repository import EventoRepository
from repositories.cotizacion_repository import CotizacionRepository
from services.calendario_service import CalendarioService
from services.tarifa_service import TarifaService
from core.enums import TipoHorario


class EventoService:
    """Servicio para calculo y persistencia de eventos dentro de una cotizacion."""

    def __init__(self, session: Session):
        self.session = session
        self.evento_repo = EventoRepository(session)
        self.cotizacion_repo = CotizacionRepository(session)
        self.calendario_service = CalendarioService(session)
        self.tarifa_service = TarifaService(session)

    def calcular_y_guardar_evento(
        self,
        cotizacion_id: int,
        servicio_id: int,
        ciudad_id: int,
        fecha: Any,
        hora_inicio: Any,
        hora_fin: Any,
        direccion: str,
        contacto: str,
        telefono: str,
        observaciones: str = "",
        extras_data: List[Dict[str, Any]] = None,
        evento_id: int = None
    ) -> Evento:
        """
        Calcula automaticamente las franjas horarias y tarifas de un evento,
        acumula los extras y actualiza los totales del evento y de la cotizacion.
        """
        cotizacion = self.cotizacion_repo.get_by_id_or_fail(cotizacion_id)

        # 1. Determinar tipo de dia (ORDINARIO vs FESTIVO)
        tipo_dia = self.calendario_service.determinar_tipo_dia(fecha)

        # 2. Calcular horas diurnas y nocturnas
        horas_diurnas, horas_nocturnas = self.calendario_service.calcular_horas_diurnas_nocturnas(
            fecha, hora_inicio, hora_fin
        )

        # 3. Obtener tarifa diurna y nocturna aplicable
        tarifa_diurna_val = 0.0
        tarifa_nocturna_val = 0.0

        if horas_diurnas > 0:
            tarifa_d = self.tarifa_service.obtener_tarifa_aplicable(
                cliente_id=cotizacion.cliente_id,
                ciudad_id=ciudad_id,
                servicio_id=servicio_id,
                tipo_dia=tipo_dia,
                tipo_horario=TipoHorario.DIURNO,
                fecha_evaluacion=fecha
            )
            tarifa_diurna_val = float(tarifa_d.valor_hora)

        if horas_nocturnas > 0:
            tarifa_n = self.tarifa_service.obtener_tarifa_aplicable(
                cliente_id=cotizacion.cliente_id,
                ciudad_id=ciudad_id,
                servicio_id=servicio_id,
                tipo_dia=tipo_dia,
                tipo_horario=TipoHorario.NOCTURNO,
                fecha_evaluacion=fecha
            )
            tarifa_nocturna_val = float(tarifa_n.valor_hora)

        valor_diurnas = round(horas_diurnas * tarifa_diurna_val, 2)
        valor_nocturnas = round(horas_nocturnas * tarifa_nocturna_val, 2)

        # 4. Procesar extras
        suma_extras = 0.0
        objetos_extras = []
        if extras_data:
            for extra_dict in extras_data:
                monto = float(extra_dict["valor"])
                suma_extras += monto
                objetos_extras.append(
                    ExtraEvento(
                        tipo=extra_dict["tipo"],
                        descripcion=extra_dict["descripcion"],
                        valor=monto
                    )
                )

        valor_total_evento = round(valor_diurnas + valor_nocturnas + suma_extras, 2)

        # 5. Crear o actualizar entidad Evento
        if evento_id:
            evento = self.evento_repo.get_by_id_or_fail(evento_id)
            evento.servicio_id = servicio_id
            evento.ciudad_id = ciudad_id
            evento.fecha = fecha
            evento.hora_inicio = hora_inicio
            evento.hora_fin = hora_fin
            evento.direccion = direccion
            evento.contacto = contacto
            evento.telefono = telefono
            evento.observaciones = observaciones
            evento.tipo_dia = tipo_dia
            evento.horas_diurnas = horas_diurnas
            evento.horas_nocturnas = horas_nocturnas
            evento.valor_horas_diurnas = valor_diurnas
            evento.valor_horas_nocturnas = valor_nocturnas
            evento.valor_extras = suma_extras
            evento.valor_evento = valor_total_evento

            # Reemplazar extras
            evento.extras.clear()
            evento.extras.extend(objetos_extras)
        else:
            # Calcular proximo orden
            num_eventos = len(cotizacion.eventos)
            evento = Evento(
                cotizacion_id=cotizacion_id,
                servicio_id=servicio_id,
                ciudad_id=ciudad_id,
                fecha=fecha,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                direccion=direccion,
                contacto=contacto,
                telefono=telefono,
                observaciones=observaciones,
                tipo_dia=tipo_dia,
                horas_diurnas=horas_diurnas,
                horas_nocturnas=horas_nocturnas,
                valor_horas_diurnas=valor_diurnas,
                valor_horas_nocturnas=valor_nocturnas,
                valor_extras=suma_extras,
                valor_evento=valor_total_evento,
                orden=num_eventos + 1,
                extras=objetos_extras
            )
            self.evento_repo.create(evento)

        self.session.flush()

        # 6. Recalcular totales de la cotizacion
        self.recalcular_totales_cotizacion(cotizacion_id)

        return evento

    def recalcular_totales_cotizacion(self, cotizacion_id: int) -> None:
        """Recalcula subtotal, extras y gran total de una cotizacion."""
        cotizacion = self.cotizacion_repo.get_by_id_or_fail(cotizacion_id)
        subtotal = 0.0
        extras_totales = 0.0

        for ev in cotizacion.eventos:
            subtotal += float(ev.valor_horas_diurnas) + float(ev.valor_horas_nocturnas)
            extras_totales += float(ev.valor_extras)

        cotizacion.valor_subtotal = round(subtotal, 2)
        cotizacion.valor_extras = round(extras_totales, 2)
        cotizacion.valor_total = round(subtotal + extras_totales, 2)
        self.session.flush()
