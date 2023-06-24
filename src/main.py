#!/usr/bin/env python
"""
cli for the main page
"""

from pathlib import Path
from typer.core import TyperGroup
import typer
from click import Context
from typing_extensions import Annotated
from config import LOGLEVEL
import advanced
import batch
import global_vars
import mpirun
from mpi4py import MPI


app = typer.Typer()


@app.command()
def simple():
    """
    This performs a benchmark run
    with sensible defaults.
    Use this if you just want to
    quickly run your benchmark.
    """
    batch.BatchScript(slurm_model=mpirun.MPIRunModel()).run()


app.add_typer(
    advanced.app,
    name="advanced",
    help="This performs a configurable benchmark run."
    + " "
    + "Use this if you want more fine grained control of the script.",
)


@app.callback()
def main(
    loglevel: Annotated[
        LOGLEVEL,
        typer.Option("--loglevel", "-l", help="adjust chattyness of app"),
    ] = LOGLEVEL.INFO.value,
    mpirun_path: Annotated[
        Path,
        typer.Option(
            "--srun-path",
            "-mr",
            help="what command to use for mpirun",
        ),
    ] = "mpirun",
    numio_path: Annotated[
        Path,
        typer.Option(
            "--numio-path",
            "-nio",
            help="what command to use for numio, "
            + "should work for all different ones "
            + "such as numio-adios2 or numio-posix",
        ),
    ] = "numio-posix",
    nodes: Annotated[
        int,
        typer.Option(
            "--node-count",
            "-n",
            help=(
                "how many nodes should be used for this test, "
                "if not specified then mpirun will pick for you"
            ),
        ),
    ] = None,
):
    """
    this is a script designed to help you quickly run numio benchmarks.
    it tries to simulate realistic test conditions
    by creating disk and network load.
    these are shared resources,
    so performance issues related to them would be hard to find
    using an isolated program.

    """
    loglevel.init_logging()
    global_vars.NUMIO_PATH = numio_path
    global_vars.MPIRUN_PATH = mpirun_path

    # if not specified get node count form mpi
    if nodes is None or nodes <= 0:
        global_vars.NODE_COUNT = MPI.COMM_WORLD.size
        print(global_vars.NODE_COUNT)
    else:
        global_vars.NODE_COUNT = nodes


if __name__ == "__main__":
    app()
