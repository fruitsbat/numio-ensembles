"""
slurm specific things
"""

from dataclasses import dataclass
import rich
from rich.columns import Columns
from rich.panel import Panel

import global_vars
import pretty_print


@dataclass
class SlurmModel:
    """
    stores srun cli args
    """

    partition: str = "west"
    nodes: int = 2
    tasks_per_node: int = 1
    tasks: int = 2
    timeout: int = 1

    def print(self) -> None:
        """
        pretty print this to the terminal
        """
        pretty_print.print_boxes(
            "slurm settings",
            [
                (" ".join(self.generate_args()), "command"),
                (self.partition, "partition"),
                (str(self.nodes), "nodes"),
                (str(self.tasks_per_node), "tasks per node"),
                (str(self.tasks), "total tasks"),
                (str(self.timeout), "timeout"),
            ],
        )

    def generate_args(self) -> [str]:
        """
        arguments to use srun
        """
        return [
            str(global_vars.SRUN_PATH),
            f"--partition={self.partition}",
            f"--ntasks-per-node={self.tasks_per_node}",
            f"--nodes={self.nodes}",
        ]
