"""
stores some global variables set by callbacks
"""

from pathlib import Path
from typing import Optional

MPIRUN_PATH: Path = "mpirun"
NUMIO_PATH: Path = "numio"
NODE_COUNT: Optional[int] = None
