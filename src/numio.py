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

    frequency: int = 1
    filepath: os.path = "path.out"

    def generate_args(self) -> [str]:
        """
        args for reading
        """
        return [
            "-r",
            (f"freq={self.frequency}," f"path={self.filepath}"),
        ]

    def printables(self) -> [(str, str)]:
        """
        get printables for this
        """
        return [
            (str(self.frequency), "frequency"),
            (str(self.filepath), "read path"),
        ]


@dataclass
class MatrixModel:
    """
    models how the matrix works that gets calculated in NumIO
    """

    iterations: int = 200000
    size: int = 5000
    use_perturbation_function: bool = True

    def printables(self) -> [(str, str)]:
        """
        get printables for this
        """
        return [
            (str(self.iterations), "iterations"),
            (f"[cyan]{self.size}[/]x[cyan]{self.size}[/]", "matrix size"),
            (
                "(f,x) = 2 * pi^2 * sin(pi * x) * sin(pi * y)"
                if self.use_perturbation_function
                else "(f,x) = 0",
                "perturbation function",
            ),
        ]

    def generate_args(self) -> [str]:
        """
        get args to control the matrix
        """
        return [
            "-m",
            (
                f"iter={self.iterations},"
                f"size={self.size},"
                f"pert={2 if self.use_perturbation_function else 1}"
            ),
        ]


@dataclass
class WriteModel:
    """
    how numio writes data
    """

    frequency: int = 1
    immediate_write: bool = False
    filesync: bool = True
    pattern: str = ""
    filepath: os.path = "path.out"

    def printables(self) -> [(str, str)]:
        """
        get printables for this
        """
        return [
            (str(self.frequency), "frequency"),
            (str(self.filepath), "read path"),
            ("[red]off[/]" if self.filesync else "[green]on[/]", "write sync"),
            (self.pattern if self.pattern else "[red]none[/]", "pattern"),
            (str(self.filepath), "write path"),
        ]

    def generate_args(self) -> [str]:
        """
        cli args for controlling writing
        """
        return [
            "-w",
            (
                f"freq={self.frequency},"
                f"path={self.filepath}"
                + (
                    ""
                    if self.filesync
                    else ",nofilesync" f'pattern="{self.pattern}"'
                )
                + (",imm" if self.immediate_write else "")
            ),
        ]


@dataclass
class CommunicationModel:
    """
    how numio fakes communication
    """

    frequency: int = 1
    size_in_kb: int = 1

    def printables(self) -> [(str, str)]:
        """
        get printables for this
        """
        return [
            (str(self.frequency), "communication frequency"),
            (f"{self.size_in_kb}kb", "size"),
        ]

    def generate_args(self) -> [str]:
        """
        cli args for controlling writing
        """
        return [
            "-c",
            (f"freq={self.frequency}," f"size={self.size_in_kb}"),
        ]


@dataclass
class NumioModel:
    """
    stores cli args for numio
    """

    command: str = "numio-posix"
    threads: int = 1
    per_process_writing: bool = False

    matrix_model: MatrixModel = MatrixModel()
    read_model: Optional[ReadModel] = ReadModel()
    write_model: Optional[WriteModel] = WriteModel()
    communication_model: Optional[CommunicationModel] = CommunicationModel()

    def print(self) -> None:
        """
        pretty print this to the terminal
        """
        printables: [(str, str)] = (
            [(" ".join(self.generate_args()), "command")]
            + self.matrix_model.printables()
            + (
                self.read_model.printables()
                if self.read_model
                else [("[red]off[/]", "reading")]
            )
            + (
                self.write_model.printables()
                if self.write_model
                else [("[red]off[/]", "writing")]
            )
            + (
                self.communication_model.printables()
                if self.communication_model
                else [("[red]off[/]", "fake communication")]
            )
        )
        pretty_print.print_boxes("NumIO settings", printables)

    def generate_args(self) -> [str]:
        """
        numio args
        """
        args = [
            f"{global_vars.NUMIO_PATH}",
        ] + self.matrix_model.generate_args()

        if self.read_model:
            args = args + self.read_model.generate_args()

        if self.write_model:
            args = args + self.write_model.generate_args()

        args = args + ["-t", str(self.threads)]

        logging.debug("numio args: %s", args)

        return args
