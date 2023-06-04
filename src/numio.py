"""
things for working with numio
"""

from dataclasses import dataclass

import global_vars
import pretty_print


@dataclass
class NumioModel:
    """
    stores cli args for numio
    """

    command: str = "numio-posix"
    iterations: int = 200000
    matrix_size: int = 5000
    use_perturbation_function: bool = True

    def print(self) -> None:
        """
        pretty print this to the terminal
        """
        pretty_print.print_boxes(
            "NumIO settings",
            [
                (" ".join(self.generate_args()), "command"),
                (str(self.iterations), "iterations"),
                (
                    f"{self.matrix_size} x {self.matrix_size}",
                    "matrix size",
                ),
                (
                    "f(x,y) = 2 * pi^2 * sin(pi * x) * sin(pi * y)"
                    if self.use_perturbation_function
                    else "f(x,y) = 0",
                    "perturbation function",
                ),
            ],
        )

    def generate_args(self) -> [str]:
        """
        numio args
        """
        return [
            f"{global_vars.NUMIO_PATH}",
            "-m",
            f"iter={self.iterations},"
            + f"size={self.matrix_size},"
            + f"pert={2 if self.use_perturbation_function else 1}",
        ]
