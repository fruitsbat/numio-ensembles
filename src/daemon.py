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
        result = subprocess.run(
                MPIRunModel().generate_args() + self.commands,
                check=True,
                capture_output=True,
        ),
        
        # start this again when it finishes
        logging.info("process of type: " + self.name + " has finished")
        if  result[0].returncode == 0:
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
    """
    return Daemon(
        commands=["sleep", "5000"],
        name="sleepy",
    )


def chatty() -> Daemon:
    """
    a very talkative daemon, uses a lot of network
    """
    return Daemon(
        commands=NumioModel(
            communication_model=CommunicationModel(size_in_kb=100000),
            matrix_model=MatrixModel(iterations=200000, size=9, use_perturbation_function=False),
        ).generate_args(),
        name="chatty",
    )

def cpu() -> Daemon:
    """
    a daemon that uses a lot of cpu
    """
    return Daemon(
        commands=NumioModel(
            write_model=WriteModel(frequency=0,),
            communication_model=CommunicationModel(frequency=0),
            read_model=ReadModel(frequency=0),
        ).generate_args(),
        name="cpu"
    )