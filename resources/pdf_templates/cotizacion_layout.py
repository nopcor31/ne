"""
Plantilla ReportLab para la generacion del documento PDF de Cotización.
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from config.settings import settings


class CotizacionPDFBuilder:
    """Clase constructora del layout PDF de la cotización usando ReportLab."""

    def __init__(self, cotizacion, output_path: str):
        self.cotizacion = cotizacion
        self.output_path = output_path
        self.doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        self.styles = getSampleStyleSheet()

    def build(self):
        """Ensambla y genera el documento PDF."""
        story = []

        # Estilos personalizados
        style_title = ParagraphStyle(
            'TitleStyle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1B6FD8'),
            spaceAfter=6
        )
        style_subtitle = ParagraphStyle(
            'SubTitleStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=12
        )
        style_heading = ParagraphStyle(
            'HeadingStyle',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#111827'),
            spaceBefore=12,
            spaceAfter=6
        )
        style_body = ParagraphStyle(
            'BodyStyle',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#374151'),
            leading=12
        )

        # 1. Encabezado Empresa y Numero de Cotizacion
        header_data = [
            [
                Paragraph(f"<b>{settings.EMPRESA_NOMBRE}</b><br/>NIT: {settings.EMPRESA_NIT}<br/>{settings.EMPRESA_DIRECCION}<br/>Tel: {settings.EMPRESA_TELEFONO}", style_body),
                Paragraph(f"<font color='#1B6FD8' size=14><b>COTIZACIÓN #{self.cotizacion.numero_cotizacion}</b></font><br/>Fecha: {self.cotizacion.fecha_creacion.strftime('%Y-%m-%d')}<br/>Estado: {self.cotizacion.estado.value}", style_body)
            ]
        ]
        header_table = Table(header_data, colWidths=[300, 240])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT')
        ]))
        story.append(header_table)
        story.append(Spacer(1, 12))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E6EC'), spaceAfter=12))

        # 2. Informacion del Cliente
        cliente = self.cotizacion.cliente
        contacto_nombre = self.cotizacion.contacto.nombre if self.cotizacion.contacto else "Atención Dirección Comercial"
        cliente_info = [
            [Paragraph(f"<b>Cliente:</b> {cliente.empresa}", style_body), Paragraph(f"<b>NIT:</b> {cliente.nit}", style_body)],
            [Paragraph(f"<b>Atención:</b> {contacto_nombre}", style_body), Paragraph(f"<b>Email:</b> {cliente.correo_principal}", style_body)],
            [Paragraph(f"<b>Teléfono:</b> {cliente.telefono_principal}", style_body), Paragraph(f"<b>Ciudad:</b> {cliente.ciudad.nombre if cliente.ciudad else ''}", style_body)]
        ]
        cliente_table = Table(cliente_info, colWidths=[270, 270])
        cliente_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F4F6FA')),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(cliente_table)
        story.append(Spacer(1, 16))

        # 3. Detalle de Eventos y Servicios
        story.append(Paragraph("Detalle de Servicios Solicitados", style_heading))
        
        table_data = [
            ["Item", "Servicio", "Fecha / Horario", "Ciudad", "Horas (D/N)", "Total Evento"]
        ]

        for idx, ev in enumerate(self.cotizacion.eventos, start=1):
            s_nombre = ev.servicio.nombre if ev.servicio else "Servicio Medico"
            c_nombre = ev.ciudad.nombre if ev.ciudad else "N/A"
            f_str = f"{ev.fecha.strftime('%Y-%m-%d')}<br/>{ev.hora_inicio.strftime('%H:%M')} - {ev.hora_fin.strftime('%H:%M')}"
            h_str = f"Diurnas: {ev.horas_diurnas}h<br/>Nocturnas: {ev.horas_nocturnas}h"
            v_str = f"${ev.valor_evento:,.2f}"

            table_data.append([
                str(idx),
                Paragraph(s_nombre, style_body),
                Paragraph(f_str, style_body),
                Paragraph(c_nombre, style_body),
                Paragraph(h_str, style_body),
                v_str
            ])

        eventos_table = Table(table_data, colWidths=[30, 150, 110, 80, 90, 80])
        eventos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1B6FD8')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E6EC')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (-1, 0), (-1, -1), 'RIGHT'),
        ]))
        story.append(eventos_table)
        story.append(Spacer(1, 12))

        # 4. Resumen Financiero
        totales_data = [
            ["Subtotal Servicios:", f"${self.cotizacion.valor_subtotal:,.2f}"],
            ["Cargos Extras / Peajes:", f"${self.cotizacion.valor_extras:,.2f}"],
            ["TOTAL A PAGAR:", f"${self.cotizacion.valor_total:,.2f}"]
        ]
        totales_table = Table(totales_data, colWidths=[400, 140])
        totales_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.HexColor('#1B6FD8')),
            ('FONTSIZE', (0, 2), (-1, 2), 11),
            ('LINEABOVE', (0, 2), (-1, 2), 1, colors.HexColor('#1B6FD8'))
        ]))
        story.append(totales_table)
        story.append(Spacer(1, 16))

        # 5. Condiciones Comerciales
        story.append(Paragraph("Condiciones Comerciales", style_heading))
        condiciones = self.cotizacion.condiciones_comerciales or settings.PDF_CONDICIONES_GENERALES
        story.append(Paragraph(condiciones.replace('\n', '<br/>'), style_body))

        # Generar archivo
        self.doc.build(story)
