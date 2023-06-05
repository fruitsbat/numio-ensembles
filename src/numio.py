"""
things for working with numio
"""

from dataclasses import dataclass
from typing import Optional
import os
import logging

import global_vars
import pretty_print


@dataclass
class ReadModel:
    """
    functionality for reading
    """

    read_frequency: int = 1
    read_path: os.path = "path.out"

    def generate_args(self) -> [str]:
        """
        args for reading
        """
        return [
            "-r",
            (f"freq={self.read_frequency}," f"path={self.read_path}"),
        ]


@dataclass
class NumioModel:
    """
    stores cli args for numio
    """

    command: str = "numio-posix"
    iterations: int = 200000
    matrix_size: int = 5000
    use_perturbation_function: bool = True
    write_frequency: int = 1
    immediate_write: bool = False
    filesync: bool = True
    pattern: str = ""
    write_path: os.path = "path.out"
    communication_frequency: int = 1
    communication_size: int = 1000
    threads: int = 1
    per_process_writing: bool = False
    read_model: Optional[ReadModel] = None

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
                (str(self.write_frequency), "write frequency"),
                (
                    f"[green]{self.immediate_write}[/]"
                    if self.immediate_write
                    else f"[red]{self.immediate_write}[/]",
                    "immediate write",
                ),
            ],
        )

    def generate_args(self) -> [str]:
        """
        numio args
        """
        args = [
            f"{global_vars.NUMIO_PATH}",
            "-m",
            f"iter={self.iterations},"
            + f"size={self.matrix_size},"
            + f"pert={2 if self.use_perturbation_function else 1}",
            "-w",
            (
                f"freq={self.write_frequency},"
                f"path={self.write_path}"
                + (
                    ""
                    if self.filesync
                    else ",nofilesync" f'pattern="{self.pattern}"'
                )
                + (",imm" if self.immediate_write else "")
            ),
            "-c",
            (
                f"freq={self.communication_frequency},"
                f"size={self.communication_size}"
            ),
            "-t",
            str(self.threads),
        ] + (self.read_model.generate_args() if self.read_model else [])
        logging.debug("numio args: %s", args)
        return args
