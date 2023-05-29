"""
this module defines the cli interface for advanced mode
"""

import typer


app = typer.Typer()


@app.command()
def empty():
    """
    A benchmark that puts low stress on the system.
    """


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
