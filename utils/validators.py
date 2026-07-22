"""
Utilidades de validación de datos (NIT, Email, Telefono).
"""

import re


def validar_email(email: str) -> bool:
    """Valida la sintaxis de un correo electronico."""
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(patron, email)) if email else False


def validar_nit(nit: str) -> bool:
    """Valida que un NIT tenga el formato colombiano o numérico adecuado."""
    if not nit:
        return False
    nit_limpio = re.sub(r"[^\d]", "", nit)
    return len(nit_limpio) >= 7
