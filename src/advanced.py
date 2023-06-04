"""
this module defines the cli interface for advanced mode
"""

import typer
import batch
import numio

app = typer.Typer()


@app.command()
def empty():
    """
    A benchmark that puts low stress on the system.
    """
    batch.BatchScript(
        numio_model=numio.NumioModel(
            iterations=1,
            matrix_size=9,
            use_perturbation_function=False,
        )
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
