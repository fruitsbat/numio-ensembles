"""
helps execute batch scripts
"""

import logging
from subprocess import Popen, PIPE, STDOUT
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
            logging.info(script_results)

    def generate_script(self) -> bytes:
        """
        generate a jobscript for sbatch to run
        """
        return (
            "#!/bin/bash"
            + f"\n#SBATCH --time={self.time}"
            + f"\n#SBATCH --nodes={self.nodes}"
            + f"\n#SBATCH --ntasks-per-node={self.tasks_per_node}"
            + f"\n#SBATCH --ntasks={self.tasks}"
            + f"\n#SBATCH --partition={self.partition}"
            + "\n#SBATCH --output=/tmp/numio-ensemble-runner-job.out"
            + "\n"
            + f"\n{global_vars.SRUN_PATH} {self.command}"
        ).encode()
