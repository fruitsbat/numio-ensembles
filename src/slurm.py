"""
slurm specific things
"""

from dataclasses import dataclass
from typing import Optional
import logging

import global_vars
import pretty_print


@dataclass
class SlurmModel:
    """
    stores srun cli args
    """

    nodes: Optional[int] = None

    def print(self) -> None:
        """
        pretty print this to the terminal
        """
        pretty_print.print_boxes(
            "mpirun settings",
            [
                (" ".join(self.generate_args()), "command"),
                (str(self.nodes) if self.nodes else "all", "nodes"),
                (str(global_vars.MPIRUN_PATH), "path"),
            ],
        )

    def generate_args(self) -> [str]:
        """
        arguments to use srun
        """
        args = [
            str(global_vars.MPIRUN_PATH),
        ]

        if self.nodes:
            args = args + [
                "-n",
                str(self.nodes),
            ]

        logging.debug("mpirun args: %s", args)

        return args
