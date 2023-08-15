"""
this module defines the cli interface for advanced mode
"""

from typing_extensions import Annotated
import typer
import batch
import daemon
import numio
import mpirun

app = typer.Typer()


@app.command()
def empty():
    """
    A benchmark that puts low background stress on the system.
    """
    batch.BatchScript(
        slurm_model=mpirun.MPIRunModel(),
        numio_model=numio.NumioModel(),
    ).run()


@app.command()
def balanced():
    """
    A benchmark that puts medium stress on the system.
    """

    daemon.run(
        [
            daemon.chatty(),
            daemon.cpu(),
            daemon.disk(),
        ]
    )

    batch.BatchScript().run()


@app.command()
def peak():
    """
    A benchmark that puts a high level of stress on the system.
    """

    daemon.run(
        [
            daemon.chatty(),
            daemon.cpu(),
            daemon.disk(),
            daemon.chatty(),
            daemon.cpu(),
            daemon.disk(),
            daemon.chatty(),
            daemon.cpu(),
            daemon.disk(),
            daemon.chatty(),
            daemon.cpu(),
            daemon.disk(),
        ]
    )

    batch.BatchScript(
        slurm_model=mpirun.MPIRunModel(),
        numio_model=numio.NumioModel(),
    ).run()


@app.command()
def custom(
    chatty: Annotated[
        int, typer.Option("--chatty", help="how many chatty background daemons to use")
    ],
    cpu: Annotated[int, typer.Option("--cpu", help="how many cpu daemons to use")],
    disk: Annotated[int, typer.Option("--disk", help="how many disk daemons to use")],
):
    daemons = []
    daemons = daemons + [daemon.chatty()] * chatty
    daemons = daemons + [daemon.cpu()] * cpu
    daemons = daemons + [daemon.disk()] * disk

    daemon.run(daemons)

    batch.BatchScript(
        slurm_model=mpirun.MPIRunModel(),
        numio_model=numio.NumioModel(),
    ).run()
