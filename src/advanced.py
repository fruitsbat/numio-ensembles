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
    use_read: Annotated[
        bool,
        typer.Option(
            "--read",
            "-r",
            help="use read operations",
        ),
    ] = False,
    use_write: Annotated[
        bool,
        typer.Option(
            "--write",
            "-w",
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
                iterations=1,
                size=9,
                use_perturbation_function=False,
            ),
            read_model=numio.ReadModel() if use_read or use_all else None,
            write_model=numio.WriteModel() if use_write or use_all else None,
        ),
    ).run()


@app.command()
def balanced():
    """
    A benchmark that puts medium stress on the system.
    """


@app.command()
def peak():
    """
    A benchmark that puts a high level of stress on the system.
    """


@app.command()
def custom():
    """
    A fully customizable benchmark.
    """


if __name__ == "__main__":
    app()
