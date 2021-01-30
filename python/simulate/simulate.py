import os.path as path
import sys
import subprocess
from pathlib import Path

from ..parameter_grid import ParameterGrid

# Example of run:
# simlord -n 100000 -fl 100 \
#   --read-reference ./data/preprocess/preprocessed.fasta \
#   ./data/simulated/simulated


grid_params = {
  # Number of reads to simulate.
  # -n
  'num_reads': [10000, 20000, 50000],

  # Length of reads
  # -fl
  'read_length': [100, 700],
}


def get_fasta_file_path(data_folder: str):
  fastq_filename = f'preprocessed.fasta'

  return path.join(data_folder, 'preprocess', fastq_filename)


def get_output_folder(data_folder: str, num_reads: int, read_length: int):
  prefix = f'n-{num_reads}-fl-{read_length}'
  return path.join(data_folder, 'simulated', f'{prefix}')


def create_simlord_params(data_folder: str, num_reads: int, read_length: int):
  fastq_file_path = get_fasta_file_path(data_folder)

  simlord_params = [
    f'--read-reference {fastq_file_path}',
    f'-n {num_reads}',
    f'-fl {read_length}',
  ]

  output_folder = get_output_folder(data_folder, num_reads, read_length)
  
  return simlord_params, output_folder


def run_simulate_reads(data_folder: str, comb):
  params, output_folder = create_simlord_params(data_folder, **comb)
  print(f'Params: {params}')
  print(f'Output: {output_folder}')                                                   
  print(f'Running SimLoRD...')

  Path(output_folder).mkdir(parents=True, exist_ok=True)
  subprocess.call(' '.join(['simlord', *params, f'{output_folder}/simulated']), shell=True)


def simulate(data_folder: str, grid_params=grid_params):
  grid = ParameterGrid(grid_params)

  for i, comb in enumerate(grid):
    run_simulate_reads(data_folder, comb)
    print(f'Iteration #{i} complete!\n\n')
