"""
things for working with numio
"""

from dataclasses import dataclass
from rich.table import Table
from rich.console import Console

import global_vars


@dataclass
class NumioModel:
    """
    stores cli args for numio
    """

    command: str = "numio-posix"
    numio_iter: int = 200000
    matrix_size: int = 5000
    use_perturbation_function: bool = True

    def print(self) -> None:
        """
        pretty print this to the terminal
        """
        table = Table(title="NumIO")
        table.add_column("Data")
        table.add_column("Value")
        table.add_row("iterations", str(self.numio_iter))
        table.add_row("matrix size", f"{self.matrix_size}x{self.matrix_size}")
        table.add_row(
            "perturbation function",
            "f(x,y) = 0"
            if not self.use_perturbation_function
            else "f(x,y) = 2 * pi^2 * sin(pi * x) * sin(pi * y)",
        )
        Console().print(table)

    def generate_args(self) -> [str]:
        """
        numio args
        """
        return [
            f"{global_vars.NUMIO_PATH}",
            "-m",
            f"iter={self.numio_iter},"
            + f"size={self.matrix_size},"
            + f"pert={1 if self.use_perturbation_function else 0}",
        ]
