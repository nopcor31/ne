"""
Controlador MVC para la administracion y calculo de Tarifas con señales Qt.
"""

from typing import Optional
from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from repositories.tarifa_repository import TarifaRepository
from services.tarifa_service import TarifaService
from services.dto.tarifa_dto import CalculoTarifaInputDTO, ResultadoCalculoTarifaDTO


class TarifaController(QObject):
    """Controlador para consulta, administracion y calculo dinamico de tarifas mediante señales Qt."""

    tarifas_cargadas = Signal(list)
    tarifa_calculada = Signal(object)
    tarifa_guardada = Signal(object)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot()
    def obtener_tarifas_generales(self):
        """Obtiene la lista de tarifas base de la empresa."""
        try:
            with session_manager.session_scope() as session:
                repo = TarifaRepository(session)
                tarifas = repo.get_all()
                self.tarifas_cargadas.emit(tarifas)
                return tarifas
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def obtener_tarifas_cliente(self, cliente_id: int):
        """Obtiene la lista de tarifas especificas configuradas para un cliente."""
        try:
            with session_manager.session_scope() as session:
                service = TarifaService(session)
                tarifas = service.obtener_tarifas_cliente(cliente_id)
                self.tarifas_cargadas.emit(tarifas)
                return tarifas
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(object)
    def calcular_tarifa_evento(self, dto: CalculoTarifaInputDTO) -> ResultadoCalculoTarifaDTO:
        """Calcula el costo total y desglose de un evento segun el motor de tarifas y reglas de negocio."""
        try:
            with session_manager.session_scope() as session:
                service = TarifaService(session)
                resultado = service.calcular_tarifa_evento(dto)
                self.tarifa_calculada.emit(resultado)
                return resultado
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(object, int, float, float, int)
    def crear_o_actualizar_tarifa(
        self,
        cliente_id: Optional[int],
        servicio_id: int,
        valor_hora: float,
        valor_dia: float,
        usuario_id: int
    ):
        """Crea o actualiza una tarifa comercial."""
        try:
            with session_manager.session_scope() as session:
                service = TarifaService(session)
                tarifa = service.crear_o_actualizar_tarifa(
                    cliente_id=cliente_id,
                    servicio_id=servicio_id,
                    valor_hora=valor_hora,
                    valor_dia=valor_dia,
                    usuario_id=usuario_id
                )
                self.tarifa_guardada.emit(tarifa)
                return tarifa
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
