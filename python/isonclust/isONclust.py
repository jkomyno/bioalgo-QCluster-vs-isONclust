import subprocess
from os import path
from glob import glob
from pathlib import Path
from ..parameter_grid import ParameterGrid

# Example of run:
# isONclust --t 1 --k 3 --w 20 --batch_type total_nt \
#   --aligned_threshold 0.4 --min_prob_no_hits 0.1 \
#   --fastq ./data/ecoli/simulated/simulated_aligned_reads.fastq \
#   --outfolder ./data/ecoli/isONclust/k3-w20-total_nt

default_const_params = {
  # Minimum aligned fraction of read to be included in cluster.
  # Aligned identity depends on the quality of the read.
  # --aligned_threshold
  'aligned_threshold': 0.4,

  # Number of CPU cores allocated for clustering.
  # --t
  'num_cores': 2,

  # Minimum probability for i consecutive minimizers to be
  # different between read and representative and still
  # considered as mapped region, under assumption that
  # they come from the same transcript (depends on read quality).
  # --min_prob_no_hits
  'min_prob_no_hits': 0.1,
}


default_grid_params = {
  # Length of word.
  # --k
  'kmer_length': [4, 5, 6, 7, 8, 9, 10, 11],

  # Window size.
  # --w
  'window': [20, 50],
}

def get_fastq_file_path(simulated_dataset_folder):
  return path.join(simulated_dataset_folder, 'simulated.fastq')


def get_output_folder(data_folder, simulated_dataset_folder, kmer_length, window):
  prefix = f'k-{kmer_length}-w-{window}'
  simulated_dataset_folder_basename = path.basename(simulated_dataset_folder)

  Path(path.join(data_folder, 'isONclust', simulated_dataset_folder_basename)) \
    .mkdir(parents=True, exist_ok=True)

  return path.join(data_folder, 'isONclust', simulated_dataset_folder_basename, f'{prefix}')


def create_isoncluster_params(data_folder: str, simulated_dataset_folder: str,
                              kmer_length: int, window: int,
                              aligned_threshold: float, num_cores: int, min_prob_no_hits: float):
  fastq_file_path = get_fastq_file_path(simulated_dataset_folder)

  isoncluster_params = [
    f'--t {num_cores}',
    f'--k {kmer_length}',
    f'--w {window}',
    f'--aligned_threshold {aligned_threshold}',
    f'--min_prob_no_hits {min_prob_no_hits}',
    f'--fastq {fastq_file_path}',
    '--outfolder',
  ]

  output_folder = get_output_folder(data_folder, simulated_dataset_folder, kmer_length, window)
  
  return isoncluster_params, output_folder


def run_cluster(data_folder: str, simulated_dataset_folder: str, comb, const_params):
  params, output_folder = create_isoncluster_params(data_folder, simulated_dataset_folder, **comb, **const_params)
  print(f'Params: {params}')
  print(f'Output: {output_folder}')                                                   
  print(f'Running isONclust...')

  subprocess.call(' '.join(['/isONclust/isONclust', *params, output_folder]), shell=True)


def isONclust(data_folder: str, 
              grid_params=default_grid_params, const_params=default_const_params):
  grid = ParameterGrid(grid_params)
  simulated_folder = path.join(data_folder, 'simulated', '*')

  for simulated_dataset_folder in glob(simulated_folder):
    for i, comb in enumerate(grid):
      run_cluster(data_folder, simulated_dataset_folder, comb, const_params)
      print(f'Iteration #{i} complete!\n\n')
