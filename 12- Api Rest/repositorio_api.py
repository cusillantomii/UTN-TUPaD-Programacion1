"""Permite importar el repositorio del TP 11 sin copiarlo.

La ruta se calcula desde este archivo, por lo que no depende de la carpeta
desde la que se ejecute Python. La base predeterminada también es la del TP 11.
"""

from pathlib import Path
import sys


RUTA_TP_DATOS = Path(__file__).resolve().parent.parent / "11 - Acceso a Datos"
if str(RUTA_TP_DATOS) not in sys.path:
    sys.path.insert(0, str(RUTA_TP_DATOS))

# Importamos después de incorporar la carpeta que contiene el paquete.
from biblioteca.repositorio import RepositorioBiblioteca
