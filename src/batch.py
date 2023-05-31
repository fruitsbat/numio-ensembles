"""
helps execute batch scripts
"""

import logging
from subprocess import Popen, PIPE
import global_vars


class BatchScript:
    """
    represents a slurm batch script in python
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        partition: str = "west",
        nodes: int = 2,
        tasks_per_node: int = 5,
        tasks: int = 10,
        time: int = 1,
        command: str = "hostname",
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
        with Popen(
            [global_vars.SBATCH_PATH],
            stdout=PIPE,
            stdin=PIPE,
            stderr=PIPE,
        ) as script_handle:
            script_results = script_handle.communicate(
                input=self.generate_script(),
            )

            if script_results[0]:  # log stdout
                logging.info(script_results[0].decode())
            if script_results[1]:  # log stderr
                logging.error(
                    "[bold red]failed to run sbatch job:[/] %s",
                    script_results[1].decode(),
                )

    def generate_script(self) -> bytes:
        """
        generate a jobscript for sbatch to run.
        this is basically the same as telling it
        to read from a file
        """
        return (
            "#!/bin/bash"
            + f"\n#SBATCH --time={self.time}"
            + f"\n#SBATCH --nodes={self.nodes}"
            + f"\n#SBATCH --ntasks-per-node={self.tasks_per_node}"
            + f"\n#SBATCH --ntasks={self.tasks}"
            + f"\n#SBATCH --partition={self.partition}"
            + "\n#SBATCH --output=/tmp/wawa.out"
            + "\n"
            + f"\n{global_vars.SRUN_PATH} {self.command}"
        ).encode()

    def print(self) -> None:
        """
        show a table with info about this script on the command line
        """
