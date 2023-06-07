"""
this module defines the cli interface for advanced mode
"""

from typing_extensions import Annotated
import typer
import batch
import numio
import slurm

app = typer.Typer()


@app.command()
def empty(
    use_all: Annotated[
        bool,
        typer.Option(
            "--all",
            "-a",
            help="uses all operations",
        ),
    ] = False,
    use_read_write: Annotated[
        bool,
        typer.Option(
            "--read-write",
            "-r",
            help="use read and write operations",
        ),
    ] = False,
    use_communication: Annotated[
        bool,
        typer.Option(
            "--communication",
            "-c",
            help="use write operations",
        ),
    ] = False,
):
    """
    A benchmark that puts low stress on the system.
    """
    batch.BatchScript(
        slurm_model=slurm.SlurmModel(),
        numio_model=numio.NumioModel(
            matrix_model=numio.MatrixModel(
                iterations=2,
                size=9,
                use_perturbation_function=False,
            ),
            read_model=numio.ReadModel(
                frequency=2,
            )
            if use_read_write or use_all
            else None,
            write_model=numio.WriteModel(
                frequency=1,
            )
            if use_read_write or use_all
            else None,
            communication_model=numio.CommunicationModel()
            if use_communication
            else None,
        ),
    ).run()


@app.command()
def balanced():
    """
    A benchmark that puts medium stress on the system.
    """
    batch.BatchScript(
        slurm_model=slurm.SlurmModel(),
        numio_model=numio.NumioModel(
            matrix_model=numio.MatrixModel(
                size=50,
            ),
            write_model=numio.WriteModel(
                frequency=100,
            ),
            read_model=numio.ReadModel(
                frequency=101,
            ),
            communication_model=numio.CommunicationModel(
                frequency=100,
                size_in_kb=100,
            ),
        ),
    ).run()


@app.command()
def peak():
    """
    A benchmark that puts a high level of stress on the system.
    """
    batch.BatchScript(
        slurm_model=slurm.SlurmModel(),
        numio_model=numio.NumioModel(
            matrix_model=numio.MatrixModel(
                size=500,
            ),
            communication_model=numio.CommunicationModel(
                frequency=1,
                size_in_kb=100000,
            ),
            write_model=numio.WriteModel(
                frequency=1,
            ),
            read_model=numio.ReadModel(
                frequency=2,
            ),
        ),
    ).run()
