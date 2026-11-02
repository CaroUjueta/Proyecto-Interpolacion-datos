import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from datos import cargar_datos

x, y, x_ign, y_ign = cargar_datos()