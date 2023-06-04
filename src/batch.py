"""
helps execute batch scripts
"""

import logging
import time

from subprocess import Popen, PIPE
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from dateutil.relativedelta import relativedelta as rd

import global_vars
from slurm import SlurmModel
from numio import NumioModel


class BatchScript:
    """
    represents a slurm batch script in python
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        slurm_model: SlurmModel = SlurmModel(),
        numio_model: NumioModel = NumioModel(),
    ):
        """
        :param str partition: the partition to run this on
        :param int nodes: amount of nodes
        :param int tasks_per_node: how many tasks to run on each node
        :param int tasks: how many tasks to run
        :param int timeout: how long the program can take in minutes
        :param str command: what command to run
        :param int numio_iter: how many iterations numio should run
        :param int matrix_size: size of the (square) numio matrix
        """

        self.numio = numio_model
        self.slurm = slurm_model

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
            with Progress(  # show pretty spinner
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=True,
            ) as progress:
                progress.add_task(
                    description=(
                        ":play_button: Running the NumIO benchmark...\n\n"
                        "this might take a while.\n"
                        "if that's a problem for you "
                        "then try running like "
                        "[green]nohup numio-ensembles &[/]"
                    ),
                    total=None,
                )
                start_time = time.perf_counter()
                script_results = script_handle.communicate()
                time_taken = rd(seconds=time.perf_counter() - start_time)
                logging.info(
                    (
                        ":stopwatch: "
                        "finished in "
                        "[yellow]%s[/] days, "
                        "[yellow]%s[/] hours, "
                        "[yellow]%s[/] minutes "
                        "and [yellow]%s[/] seconds"
                    ),
                    time_taken.days,
                    time_taken.hours,
                    time_taken.minutes,
                    round(time_taken.seconds),
                )

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
            f"--partition={self.slurm.partition}",
            f"--ntasks-per-node={self.slurm.tasks_per_node}",
            f"--nodes={self.slurm.nodes}",
            f"{global_vars.NUMIO_PATH}",
            "-m",
            f"iter={self.numio.numio_iter},"
            + f"size={self.numio.matrix_size},"
            + f"pert={1 if self.numio.use_perturbation_function else 0}",
        ]

    def print(self) -> None:
        """
        show a table with info about this script on the command line
        """
        self.slurm.print()
        self.numio.print()
