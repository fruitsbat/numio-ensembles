#!/bin/bash
	
# Time limit is one minute. See "man sbatch" for other time formats.
#SBATCH --time=1
# Run a total of ten tasks on two nodes (that is, five tasks per node).
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks=2
# Use "west" partition.
#SBATCH --partition=west
# Output goes to "job.out", error messages to "job.err".
#SBATCH --output=job.out
#SBATCH --error=job.err

srun hostname
mpiexec ./src/main.py hostnames