"""
Excepciones personalizadas de la aplicacion CRM Operativo.

Define jerarquia de excepciones de dominio para captura explicita y
manejo limpio de errores en capas superiores.
"""

class CRMException(Exception):
    """Excepcion base para todas las excepciones del dominio CRM."""
    def __init__(self, mensaje: str, codigo: str = "ERROR_CRM"):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self) -> str:
        return f"[{self.codigo}] {self.mensaje}"


class EntidadNoEncontradaError(CRMException):
    """Lanzada cuando no se encuentra un registro especifico en la base de datos."""
    def __init__(self, entidad: str, identificador: str | int):
        mensaje = f"{entidad} con ID/Codigo '{identificador}' no fue encontrado."
        super().__init__(mensaje, codigo="ENTIDAD_NO_ENCONTRADA")


class TarifaNoEncontradaError(CRMException):
    """Lanzada cuando no existe una tarifa aplicable para la combinacion requerida."""
    def __init__(self, ciudad: str, servicio: str, tipo_dia: str, tipo_horario: str):
        mensaje = (
            f"No se encontro tarifa vigente para {servicio} en {ciudad} "
            f"({tipo_dia} / {tipo_horario})."
        )
        super().__init__(mensaje, codigo="TARIFA_NO_ENCONTRADA")


class TransicionInvalidaError(CRMException):
    """Lanzada cuando se intenta una transicion de estado no permitida por la maquina de estados."""
    def __init__(self, estado_actual: str, estado_nuevo: str, id_cotizacion: int):
        mensaje = (
            f"Transicion invalida para Cotizacion #{id_cotizacion}: "
            f"no se puede pasar de '{estado_actual}' a '{estado_nuevo}'."
        )
        super().__init__(mensaje, codigo="TRANSICION_INVALIDA")


class ValidacionError(CRMException):
    """Lanzada cuando los datos proporcionados no cumplen las reglas de validacion."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="ERROR_VALIDACION")


class IntegracionOutlookError(CRMException):
    """Lanzada cuando falla la comunicacion COM con Microsoft Outlook."""
    def __init__(self, mensaje: str):
        super().__init__(f"Error de integracion con Outlook: {mensaje}", codigo="ERROR_OUTLOOK")


class GeneracionPDFError(CRMException):
    """Lanzada cuando ocurre un error durante la construccion del documento PDF."""
    def __init__(self, mensaje: str):
        super().__init__(f"Error al generar el PDF de la cotizacion: {mensaje}", codigo="ERROR_PDF")


class ReglaNegocioError(CRMException):
    """Lanzada cuando se vulnera una regla de negocio del sistema."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo="REGLA_NEGOCIO_VIOLADA")
