"""
Servicio para la construccion de documentos PDF con ReportLab.
"""

from pathlib import Path
from sqlalchemy.orm import Session
from repositories.cotizacion_repository import CotizacionRepository
from resources.pdf_templates.cotizacion_layout import CotizacionPDFBuilder
from config.settings import settings
from core.exceptions import GeneracionPDFError
from loguru import logger


class PDFService:
    """Servicio encargado de generar archivos PDF de cotizaciones."""

    def __init__(self, session: Session):
        self.session = session
        self.cotizacion_repo = CotizacionRepository(session)

    def generar_pdf_cotizacion(self, cotizacion_id: int) -> str:
        """
        Genera el documento PDF formal para una cotizacion dada.
        
        Returns:
            str: Ruta absoluta al archivo PDF generado.
        """
        cotizacion = self.cotizacion_repo.obtener_con_detalles(cotizacion_id)
        if not cotizacion:
            raise GeneracionPDFError(f"No se encontro la cotizacion #{cotizacion_id}")

        nombre_archivo = f"cotizacion_{cotizacion.numero_cotizacion}.pdf"
        ruta_destino = settings.OUTPUT_DIR / nombre_archivo

        try:
            builder = CotizacionPDFBuilder(cotizacion, str(ruta_destino))
            builder.build()

            cotizacion.pdf_path = str(ruta_destino)
            self.session.flush()

            logger.info(f"PDF generado exitosamente para Cotizacion #{cotizacion.numero_cotizacion}: {ruta_destino}")
            return str(ruta_destino)
        except Exception as exc:
            logger.error(f"Error generando PDF para Cotizacion #{cotizacion_id}: {exc}")
            raise GeneracionPDFError(str(exc))
