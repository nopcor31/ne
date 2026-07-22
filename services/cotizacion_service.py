"""
Servicio para la gestion del ciclo de vida de las Cotizaciones.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from models.cotizacion import Cotizacion
from repositories.cotizacion_repository import CotizacionRepository
from services.historial_service import HistorialService
from utils.numero_generador import NumeroGenerador
from core.enums import EstadoCotizacion


class CotizacionService:
    """Servicio para la administracion de expedientes de cotizacion."""

    def __init__(self, session: Session):
        self.session = session
        self.cotizacion_repo = CotizacionRepository(session)
        self.historial_service = HistorialService(session)

    def crear_borrador(
        self,
        cliente_id: int,
        usuario_creador_id: int,
        contacto_id: Optional[int] = None,
        observaciones: Optional[str] = None,
        condiciones_comerciales: Optional[str] = None
    ) -> Cotizacion:
        """Crea una nueva cotizacion en estado BORRADOR con numero consecutivo unico."""
        numero = NumeroGenerador.generar_numero_cotizacion(self.session)

        cotizacion = Cotizacion(
            numero_cotizacion=numero,
            cliente_id=cliente_id,
            contacto_id=contacto_id,
            estado=EstadoCotizacion.BORRADOR,
            usuario_creador_id=usuario_creador_id,
            observaciones=observaciones,
            condiciones_comerciales=condiciones_comerciales,
            valor_subtotal=0.0,
            valor_extras=0.0,
            valor_total=0.0
        )
        self.cotizacion_repo.create(cotizacion)
        self.session.flush()

        self.historial_service.registrar_accion(
            usuario_id=usuario_creador_id,
            entidad_tipo="cotizacion",
            entidad_id=cotizacion.id,
            accion="Cotizacion Creada",
            detalle=f"Borrador creado con numero consecutivo {numero}"
        )

        return cotizacion

    def obtener_por_id(self, cotizacion_id: int) -> Optional[Cotizacion]:
        """Obtiene una cotizacion con sus detalles completos."""
        return self.cotizacion_repo.obtener_con_detalles(cotizacion_id)

    def listar_por_estado(self, estado: EstadoCotizacion) -> List[Cotizacion]:
        """Obtiene cotizaciones filtradas por estado."""
        return self.cotizacion_repo.obtener_por_estado(estado)

    def buscar_cotizaciones(self, texto: str) -> List[Cotizacion]:
        """Busca cotizaciones por numero o por empresa."""
        return self.cotizacion_repo.buscar_por_texto(texto)
