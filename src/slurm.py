"""
slurm specific things
"""

from dataclasses import dataclass
from rich.table import Table
from rich.console import Console

import global_vars


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
        table = Table(title="slurm")
        table.add_column("Data")
        table.add_column("Value", style="green")
        table.add_row("partition", str(self.partition))
        table.add_row("tasks total", str(self.tasks))
        table.add_row("tasks per node", str(self.tasks_per_node))
        table.add_row("nodes", str(self.nodes))
        table.add_row("time before timeout", str(self.timeout))
        Console().print(table)

    def generate_args(self) -> [str]:
        """
        arguments to use srun
        """
        return [
            global_vars.SRUN_PATH,
            f"--partition={self.partition}",
            f"--ntasks-per-node={self.tasks_per_node}",
            f"--nodes={self.nodes}",
        ]
