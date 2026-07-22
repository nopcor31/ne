"""
Servicio para envio de correos electronicos mediante la API COM de Microsoft Outlook.
"""

import sys
from typing import List, Optional
from loguru import logger
from core.exceptions import IntegracionOutlookError


class OutlookEmailService:
    """Servicio para despacho de correos electronicos usando el cliente local de Outlook."""

    def __init__(self):
        self._outlook_disponible = sys.platform == "win32"

    def enviar_correo(
        self,
        destinatario: str,
        asunto: str,
        cuerpo_html: str,
        adjuntos: Optional[List[str]] = None,
        mostrar_preview: bool = False
    ) -> bool:
        """
        Envía o despliega un correo electrónico a través del cliente COM de Outlook.
        
        Args:
            destinatario (str): Dirección o lista de correos separados por coma.
            asunto (str): Asunto del mensaje.
            cuerpo_html (str): Contenido en formato HTML.
            adjuntos (List[str], optional): Lista de rutas absolutas de archivos adjuntos.
            mostrar_preview (bool): Si es True, abre la ventana de Outlook para edicion previa.
            
        Returns:
            bool: True si la operacion fue exitosa.
        """
        if not self._outlook_disponible:
            logger.warning("Integración COM con Outlook no disponible en este sistema operativo. Simulación activa.")
            return True

        try:
            import win32com.client # import dinamico
            outlook_app = win32com.client.Dispatch("Outlook.Application")
            mail_item = outlook_app.CreateItem(0)  # 0 = olMailItem

            mail_item.To = destinatario
            mail_item.Subject = asunto
            mail_item.HTMLBody = cuerpo_html

            if adjuntos:
                for ruta_adjunto in adjuntos:
                    mail_item.Attachments.Add(ruta_adjunto)

            if mostrar_preview:
                mail_item.Display()
            else:
                mail_item.Send()

            logger.info(f"Correo despachado a {destinatario} con asunto '{asunto}' via Outlook.")
            return True

        except Exception as exc:
            logger.error(f"Error al enviar correo via Outlook COM: {exc}")
            raise IntegracionOutlookError(str(exc))
