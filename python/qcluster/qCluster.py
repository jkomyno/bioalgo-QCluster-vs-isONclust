import subprocess
from os import path
from glob import glob
from pathlib import Path
from ..parameter_grid import ParameterGrid

# Example of run:
# qCluster -S 42 -R -w -c 3 -d a -k 3 -t 1 ./data/ecoli/simulated/simulated_aligned_reads.fastq
# result = subprocess.run(['qCluster', '-S 42', '-R', '-w', '-c 3', '-d a', '-k 3', '-t 1'], stdout=subprocess.PIPE, check=True)


DISTANCE_D2_STAR = 'a'
DISTANCE_CHI_SQUARE = 'c'
DISTANCE_EUCLIDEAN = 'e'

default_const_params = {
  # number of clusters.
  # -c
  'num_cluster': 100,

  # whether to redistribute missing quality among other bases or not.
  # -R
  'redistribute_quality': True,

  # write sequences from each cluster to a file.
  # -w
  'write_to_file': True,
}

default_grid_params = {
  # distance type
  # -d
  'dist_type': [
    DISTANCE_CHI_SQUARE,
    DISTANCE_EUCLIDEAN,
    DISTANCE_D2_STAR
  ],

  # length of word.
  # -k
  'kmer_length': [4, 5, 6, 7, 8, 9],
}


def get_fastq_file_path(simulated_dataset_folder: str):
  return path.join(simulated_dataset_folder, 'simulated.fastq')


def get_output_folder(data_folder: str, simulated_dataset_folder: str,
                      dist_type: str, kmer_length: int):
  prefix = f'd-{dist_type}-k-{kmer_length}'
  simulated_dataset_folder_basename = path.basename(simulated_dataset_folder)

  Path(path.join(data_folder, 'qCluster', simulated_dataset_folder_basename)) \
    .mkdir(parents=True, exist_ok=True)

  return path.join(data_folder, 'qCluster', simulated_dataset_folder_basename, f'{prefix}')


def create_qcluster_params(data_folder: str, simulated_dataset_folder: str,
                           dist_type: str, kmer_length: int, num_cluster: int,
                           redistribute_quality: bool, write_to_file: bool):
  redistribute_quality_param = '-R' if not redistribute_quality else None
  write_to_file_param = '-w' if write_to_file else None

  fastq_file_path = get_fastq_file_path(simulated_dataset_folder)

  qcluster_params = [
    f'-c {num_cluster}',
    f'-d {dist_type}',
    f'-k {kmer_length}',
    redistribute_quality_param,
    write_to_file_param,
    fastq_file_path
  ]

  # remove None params from the list
  qcluster_params = list(filter(lambda x: x is not None, qcluster_params))

  output_folder = get_output_folder(data_folder, simulated_dataset_folder, \
                                    dist_type, kmer_length)
  
  return qcluster_params, output_folder


def move_cluster_results(output_folder):
  subprocess.run(['mkdir', '-p', output_folder], check=True)
  subprocess.call(f'mv ./*.fastq {output_folder}', shell=True)
  subprocess.call(f'mv ./inferred_clusters.tsv {output_folder}', shell=True)


def run_cluster(data_folder: str, simulated_dataset_folder: str, comb, const_params):
  params, output_folder = create_qcluster_params(data_folder, simulated_dataset_folder,
                                                 **comb, **const_params)
  print(f'Params: {params}')
  print(f'Output: {output_folder}')                                                   
  print(f'Running qCluster...')

  with open('inferred_clusters.tsv', 'w') as buf:
    cmd = ['qCluster', *params]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1,
            universal_newlines=True) as p:
      for line in p.stdout:
          print(line, end='')
          buf.write(line)

  print(f'qCluster complete! Moving results')
  move_cluster_results(output_folder)


def qCluster(data_folder: str, 
             grid_params=default_grid_params, const_params=default_const_params):
  grid = ParameterGrid(grid_params)
  simulated_folder = path.join(data_folder, 'simulated', '*')

  for simulated_dataset_folder in glob(simulated_folder):
    for i, comb in enumerate(grid):
      run_cluster(data_folder, simulated_dataset_folder, comb, const_params)
      print(f'Iteration #{i} complete!\n\n')
