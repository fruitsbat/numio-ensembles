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
    # read: Annotated[bool, typer.Option("--read", "-r", "use read")] = False
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
