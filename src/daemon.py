"""
helper to start background noise jobs as daemons
"""

import logging
import threading
from typing import List
from concurrent.futures import ThreadPoolExecutor as Pool
import subprocess

from mpirun import MPIRunModel
from numio import CommunicationModel, MatrixModel, NumioModel, ReadModel, WriteModel


class Daemon:
    """
    a daemon to run.
    these are useful for creating background noise
    """

    firstRun: bool = True

    def __init__(self, commands: List[str], name: str):
        self.commands = commands
        self.name = name

    def run(self):
        if self.firstRun:
            logging.info("starting process of type: " + self.name)
        else:
            logging.info("restarting process of type: " + self.name)
        self.firstRun = False
        result = (
            subprocess.run(
                MPIRunModel().generate_args() + self.commands,
                check=True,
                capture_output=True,
            ),
        )

        logging.info("process of type: " + self.name + " has finished")
        if result[0].returncode == 0:
            # start this again when it finishes
            # to keep usage levels similar throughout benchmark
            self.run()
        else:
            logging.error("failed to run background noise daemon: " + result[0].stderr)


def run(daemons: List[Daemon]):
    """
    starts all the different daemons
    """
    for daemon in daemons:
        thread = threading.Thread(target=daemon.run)
        # daemon thread exits when main thread exits
        thread.daemon = True
        thread.start()


def sleepy() -> Daemon:
    """
    a daemon that reserves a thread but doesn't do anything
    this is for simulating an idle system
    """
    return Daemon(
        commands=["sleep", "5000"],
        name="sleepy",
    )


def chatty() -> Daemon:
    """
    a very talkative daemon, uses a lot of network
    this simulates big files being sent around
    """
    return Daemon(
        commands=NumioModel(
            # a lot of communication
            communication_model=CommunicationModel(size_in_kb=400000000, frequency=1,),
            # but not a whole lot else
            matrix_model=MatrixModel(
                size=9, use_perturbation_function=False
            ),
            write_model=None,
            read_model=None,
        ).generate_args(),
        name="chatty",
    )


def cpu() -> Daemon:
    """
    a daemon that uses a lot of cpu
    this is similar to the workload of compiling a program
    """
    return Daemon(
        commands=NumioModel(
            write_model=None,
            communication_model=None,
            read_model=None,
        ).generate_args(),
        name="cpu",
    )


def disk() -> Daemon:
    """
    a daemon that slows down diskIO
    this is similar to the workload of someone running a large grep
    """
    return Daemon(
        commands=NumioModel(
            write_model=WriteModel(frequency=1),
            read_model=ReadModel(frequency=2),
            communication_model=None,
            matrix_model=MatrixModel(
                size=9,
                use_perturbation_function=False,
            ),
        ).generate_args(),
        name="disk",
    )
