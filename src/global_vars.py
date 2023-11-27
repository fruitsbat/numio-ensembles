"""
stores some global variables set by callbacks
"""

from pathlib import Path
from mpi4py import MPI

MPIRUN_PATH: Path = Path("mpirun")
NUMIO_PATH: Path = Path("numio")
NODE_COUNT: int = 1
COMM = MPI.COMM_WORLD
PARTITION: str = "west"
