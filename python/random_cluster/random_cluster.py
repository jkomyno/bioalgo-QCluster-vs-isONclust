from pathlib import Path
from numpy.random import Generator, PCG64, SeedSequence
from os import path
from Bio import SeqIO
from typing import List, Iterable, FrozenSet, Dict, TypeVar


def get_input_fastq_file(args):
  return path.join(args.data, 'simulated', args.simulated, 'simulated.fastq')


def get_read_ids(input_fastq_file: str) -> List[str]:
  """
  Reads a fastq file and returns the set of read ids.
  The file is accessed in a streaming fashion, to avoid memory issues.
  """
  return [
    seq_record.description.split(' ')[0]
    for seq_record in SeqIO.parse(input_fastq_file, 'fastq')
  ]


T = TypeVar('T')
def divide_in_partitions(l: List[T], k: int, seed: int) -> List[FrozenSet[T]]:
  """
  Divide the given list into k random partitions
  """
  rng = Generator(PCG64(SeedSequence(seed)))
  rng.shuffle(l)
  return [frozenset(l[j::k]) for j in range(k)]


def write_clusters_to_tsv(clusters: List[FrozenSet[str]], tsv_path: str):  
  output_tsv_directory = path.dirname(tsv_path)
  Path(output_tsv_directory).mkdir(parents=True, exist_ok=True)

  with open(tsv_path, 'w') as tsv:
    for i, cluster in enumerate(clusters):
      for read_id in cluster:
        tsv.write(f'{i}\t{read_id}\n')


def random_cluster(args, seed: int):
  # - read simulated.fastq file
  # - assuming we want the resulting clustering to be balanced,
  #   we create n_clusters random clusters with roughly the same
  #   number of distinct points
  input_fastq_file = get_input_fastq_file(args)
  read_ids = get_read_ids(input_fastq_file)
  clusters = divide_in_partitions(read_ids, args.k, seed)

  tsv_path = path.join(args.data, 'random_cluster', args.simulated,
                       'inferred_clusters.tsv')

  # write_clusters_to_tsv(clusters, tsv_path)
