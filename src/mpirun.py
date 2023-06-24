"""
slurm specific things
"""

from dataclasses import dataclass
import logging
from typing import List

import global_vars
import pretty_print


@dataclass
class MPIRunModel:
    """
    stores srun cli args
    """

    def print(self) -> None:
        """
        pretty print this to the terminal
        """
        pretty_print.print_boxes(
            "mpirun settings",
            [
                (" ".join(self.generate_args()), "command"),
                (
                    str(global_vars.NODE_COUNT) if global_vars.NODE_COUNT else "1",
                    "nodes",
                ),
                (str(global_vars.MPIRUN_PATH), "path"),
            ],
        )

    def generate_args(self) -> List[str]:
        """
        arguments to use srun
        """
        args = [
            str(global_vars.MPIRUN_PATH),
            "-n",
        ]

        args = args + [
            str(global_vars.NODE_COUNT) if global_vars.NODE_COUNT else str("1")
        ]

        logging.debug("mpirun args: %s", args)

        return args
