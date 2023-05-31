"""
helps execute batch scripts
"""

import logging
from subprocess import Popen, PIPE
from rich.console import Console
from rich.table import Table
import global_vars
from numio import NumioHandle


class BatchScript:
    """
    represents a slurm batch script in python
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        partition: str = "west",
        nodes: int = 2,
        tasks_per_node: int = 1,
        tasks: int = 2,
        time: int = 1,
        command: str = "numio-posix",
    ):
        """
        :param str partition: the partition to run this on
        :param int nodes: amount of nodes
        :param int tasks_per_node: how many tasks to run on each node
        :param int tasks: how many tasks to run
        :param int time: how long the program can take in minutes
        :param str command: what command to run
        """

        self.partition = partition
        self.nodes = nodes
        self.tasks_per_node = tasks_per_node
        self.tasks = tasks
        self.time = time
        self.command = command

    def run(self):
        """
        run this batch script on the cluster
        """
        self.print()
        with Popen(
            self.generate_args(),
            stdout=PIPE,
            stdin=PIPE,
            stderr=PIPE,
        ) as script_handle:
            script_results = script_handle.communicate()

            if script_results[0]:  # log stdout
                logging.info(script_results[0].decode())
            if script_results[1]:  # log stderr
                logging.error(
                    "[bold red]failed to run sbatch job:[/] %s",
                    script_results[1].decode(),
                )

    def generate_args(self) -> []:
        """
        srun args
        """
        return [
            global_vars.SRUN_PATH,
            f"--partition={self.partition}",
            f"--ntasks-per-node={self.tasks_per_node}",
            f"--nodes={self.nodes}",
            NumioHandle().generate_command().decode(),
        ]

    def print(self) -> None:
        """
        show a table with info about this script on the command line
        """
        table = Table(title="this run")
        table.add_column("Data")
        table.add_column("Value")
        table.add_row("partition", str(self.partition))
        table.add_row("tasks total", str(self.tasks))
        table.add_row("tasks per node", str(self.tasks_per_node))
        table.add_row("nodes", str(self.nodes))
        table.add_row("time before timeout", str(self.time))
        Console().print(table)
