"""
Controlador MVC para la gestion de Cotizaciones con señales Qt.
"""

from typing import List, Optional
from PySide6.QtCore import QObject, Signal, Slot
from core.session_manager import session_manager
from services.cotizacion_service import CotizacionService
from services.estado_service import EstadoService
from services.pdf_service import PDFService
from services.outlook_email_service import OutlookEmailService
from services.dto.cotizacion_dto import CotizacionDTO
from core.enums import EstadoCotizacion


class CotizacionController(QObject):
    """Controlador orquestador del flujo comercial de Cotizaciones mediante señales Qt."""

    cotizacion_creada = Signal(int)
    estado_transicionado = Signal(object)
    pdf_generado = Signal(str)
    email_enviado = Signal(str)
    cotizaciones_cargadas = Signal(list)
    cotizacion_calculada = Signal(object)
    error_ocurrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    @Slot(int, int, object, object)
    def crear_borrador(
        self,
        cliente_id: int,
        usuario_creador_id: int,
        contacto_id: Optional[int] = None,
        observaciones: Optional[str] = None
    ) -> int:
        """Crea un borrador de cotizacion y retorna su ID."""
        try:
            with session_manager.session_scope() as session:
                service = CotizacionService(session)
                cotizacion = service.crear_borrador(
                    cliente_id=cliente_id,
                    usuario_creador_id=usuario_creador_id,
                    contacto_id=contacto_id,
                    observaciones=observaciones
                )
                self.cotizacion_creada.emit(cotizacion.id)
                return cotizacion.id
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def obtener_por_id(self, cotizacion_id: int) -> Optional[CotizacionDTO]:
        """Obtiene una cotizacion por su ID formateada como DTO."""
        try:
            with session_manager.session_scope() as session:
                service = CotizacionService(session)
                cot = service.obtener_por_id(cotizacion_id)
                return CotizacionDTO.from_model(cot) if cot else None
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(object, object)
    def listar_cotizaciones(
        self,
        estado: Optional[EstadoCotizacion] = None,
        cliente_id: Optional[int] = None
    ) -> List[CotizacionDTO]:
        """Obtiene la lista de cotizaciones con filtros opcionales."""
        try:
            with session_manager.session_scope() as session:
                service = CotizacionService(session)
                cotizaciones = service.listar_cotizaciones(estado=estado, cliente_id=cliente_id)
                dtos = [CotizacionDTO.from_model(c) for c in cotizaciones]
                self.cotizaciones_cargadas.emit(dtos)
                return dtos
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, object, int, object)
    def transicionar_estado(
        self,
        cotizacion_id: int,
        nuevo_estado: EstadoCotizacion,
        usuario_id: int,
        observacion: Optional[str] = None
    ) -> None:
        """Cambia el estado de la cotizacion siguiendo la maquina de estados."""
        try:
            with session_manager.session_scope() as session:
                estado_svc = EstadoService(session)
                transicion = estado_svc.transicionar(cotizacion_id, nuevo_estado, usuario_id, observacion)
                self.estado_transicionado.emit(transicion)
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int)
    def calcular_totales_cotizacion(self, cotizacion_id: int):
        """Recalcula subtotal, IVA y valor total de una cotizacion."""
        try:
            with session_manager.session_scope() as session:
                service = CotizacionService(session)
                cot = service.calcular_totales_cotizacion(cotizacion_id)
                self.cotizacion_calculada.emit(cot)
                return cot
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, int)
    def duplicar_cotizacion(self, cotizacion_id: int, usuario_id: int) -> int:
        """Clona una cotizacion existente en estado Borrador."""
        try:
            with session_manager.session_scope() as session:
                service = CotizacionService(session)
                nueva_cot = service.duplicar_cotizacion(cotizacion_id, usuario_id)
                self.cotizacion_creada.emit(nueva_cot.id)
                return nueva_cot.id
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, int, str)
    def cancelar_cotizacion(self, cotizacion_id: int, usuario_id: int, motivo: str):
        """Cancela una cotizacion indicando el motivo."""
        try:
            with session_manager.session_scope() as session:
                service = CotizacionService(session)
                cot = service.cancelar_cotizacion(cotizacion_id, usuario_id, motivo)
                self.estado_transicionado.emit(cot)
                return cot
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise

    @Slot(int, int)
    def generar_pdf_y_enviar_email(self, cotizacion_id: int, usuario_id: int) -> str:
        """Genera el PDF formal y lo despacha por correo via Outlook COM."""
        try:
            with session_manager.session_scope() as session:
                pdf_svc = PDFService(session)
                cot_svc = CotizacionService(session)
                estado_svc = EstadoService(session)
                email_svc = OutlookEmailService()

                # 1. Generar PDF
                pdf_path = pdf_svc.generar_pdf_cotizacion(cotizacion_id)
                self.pdf_generado.emit(pdf_path)

                # 2. Obtener cotizacion
                cot = cot_svc.obtener_por_id(cotizacion_id)
                destinatario = cot.cliente.correo_principal if cot.cliente else ""

                # 3. Enviar via Outlook
                asunto = f"Cotización de Servicios Médicos #{cot.numero_cotizacion}"
                cuerpo = (
                    f"Estimado(a) cliente,<br><br>"
                    f"Adjunto enviamos la cotización #{cot.numero_cotizacion} por un valor total de "
                    f"${cot.valor_total:,.2f} COP.<br><br>"
                    f"Atentamente,<br>Servicios Médicos NE"
                )

                if destinatario:
                    email_svc.enviar_correo(
                        destinatario=destinatario,
                        asunto=asunto,
                        cuerpo_html=cuerpo,
                        adjuntos=[pdf_path],
                        mostrar_preview=True
                    )
                    self.email_enviado.emit(destinatario)

                # 4. Transicionar estado a ENVIADA_CLIENTE
                estado_svc.transicionar(cotizacion_id, EstadoCotizacion.ENVIADA_CLIENTE, usuario_id)

                return pdf_path
        except Exception as e:
            self.error_ocurrido.emit(str(e))
            raise
