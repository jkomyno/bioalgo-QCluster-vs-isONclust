import random
import heapq
import numpy as np

from Bio import SeqIO
from itertools import groupby, tee
from typing import List, Tuple, Dict

from .functional import fst, snd


def get_key_length_pairs(input_fasta_file) -> List[Tuple[str, int]]:
  """
  Given a fasta file, it computes the (key, length) list of pairs for each sequence,
  where key is the sequence identifier and length is the length of the sequence.
  The file is accessed in a streaming fashion, to avoid memory issues.
  """
  return [
    (get_accessor(seq_record.description), len(seq_record))
    for seq_record in SeqIO.parse(input_fasta_file, 'fasta')
  ]


def cluster_by_std_dev(key_length_pairs: List[Tuple[str, int]], threshold: float) -> Dict[int, List[Tuple[str, int]]]:
  """
  Group the lengths in `key_length_pairs` according to their standard deviation.
  Two pairs are in the same cluster if the distance between their lengths is no more
  than the given standard deviation threshold removed from the mean distances between
  the lengths in the entire group.

  The result of this function is a key-value map where the key indicates the cluster id,
  and the value is the list of (sequence key, sequence length) pairs whose lengths are
  not too different from each other, according to the standard deviation criterion.
  """

  def compute_cluster_by_std_dev(key_length_pairs: List[Tuple[str, int]], threshold: float, key=snd):
    # sort the key length pairs according to their length
    data = sorted(key_length_pairs, key=key)

    # calculate the standard deviation of the gaps between two consecutive values
    # in the data
    std_dev = np.std([key(y) - key(x) for x, y in zip(data[:-1], data[1:])])

    # the first element belongs to the first cluster id, 0
    cluster_id = 0
    prev = data[0]
    yield cluster_id, prev

    for x in data[1:]:
      # if the gap from the current value to the previous is more than the given
      # standard deviation threshold, then create a new cluster
      if (key(x) - key(prev)) / std_dev > threshold:
        cluster_id += 1

      prev = x
      yield cluster_id, x
  

  # key-value map where the key `c` indicates the cluster id, and the value is the list of
  # (sequence key, sequence length) pairs whose lengths are not too different from each
  # other, according to the standard deviation criterion
  cluster_dict = {
    c: [snd(x) for x in v]
    for c, v in groupby(compute_cluster_by_std_dev(key_length_pairs, threshold=threshold), key=fst)
  }

  return cluster_dict


def select_best_sequences_from_clusters(cluster_dict: Dict[int, List[Tuple[str, int]]]) -> List[Tuple[str, int]]:
  """
  Retrieve the best sequences keys and lengths from a given cluster dictionary.
  "Best" means that the cluster with the third highest cardinality is preferred.
  This is because the cluster with the highest cardinality is composed of very short sequences,
  and the elements of the third cluster have a slightly inferior gap compared to the elements
  in the second cluster.
  """

  def select_best_indexes(data):
    indexes = heapq.nlargest(4, range(len(data)), data.__getitem__)
    return indexes


  data = list(map(len, cluster_dict.values()))
  lst  = list(map(lambda x: (len(x), x), cluster_dict.values()))

  best_indexes = select_best_indexes(data)
  first_best_idx, second_best_idx, third_best_idx, fourth_best_idx \
    = best_indexes[0], best_indexes[1], best_indexes[2], best_indexes[3]

  first_best_len, first_best_list = lst[first_best_idx]
  print(f'1st best cluster: ({first_best_len} elements)')
  print(f'    Min length: {min(first_best_list, key=snd)}')
  print(f'    Max length: {max(first_best_list, key=snd)}')
  print('')

  second_best_len, second_best_cluster = lst[second_best_idx]
  print(f'2nd best cluster: ({second_best_len} elements)')
  print(f'    Min length: {min(second_best_cluster, key=snd)}')
  print(f'    Max length: {max(second_best_cluster, key=snd)}')
  print('')

  third_best_len, third_best_cluster = lst[third_best_idx]
  print(f'3rd best cluster: ({third_best_len} elements)')
  print(f'    Min length: {min(third_best_cluster)}')
  print(f'    Max length: {max(third_best_cluster)}')
  print('')

  fourth_best_len, fourth_best_cluster = lst[fourth_best_idx]
  print(f'4th best cluster: ({fourth_best_len} elements)')
  print(f'    Min length: {min(fourth_best_cluster)}')
  print(f'    Max length: {max(fourth_best_cluster)}')
  print('')

  return third_best_cluster


def get_accessor(identifier: str) -> str:
  """
  Given a SeqRecord identifier string, return the access number as a string.
  e.g. "ENSG00000004776|ENSG00000004776.13|ENST00000004982|ENST00000004982.6" -> "ENST00000004982.6"
  """
  parts = identifier.split('|')
  assert len(parts) == 4
  return parts[3]


def save_best_sequences(best_sequences: List[Tuple[str, int]], n_sequences_to_keep: int,
                        input_fasta_file: str, output_fasta_file: str):
  fasta_header_dict = SeqIO.index(input_fasta_file, 'fasta', key_function=get_accessor)

  # extract `n_sequences_to_keep` unique header keys from `best_sequences`
  keys_to_extract: List[str] = random.sample(list(map(fst, best_sequences)), n_sequences_to_keep)

  # write the selected sequences to `output_fasta_file`
  with open(output_fasta_file, 'wb') as f:  
    for key in keys_to_extract:
      seq_record = fasta_header_dict[key]
      print(f'>{seq_record.description}')
      f.write(fasta_header_dict.get_raw(key))


def preprocess(input_fasta_file: str, output_fasta_file: str,
               n_sequences_to_keep: int, std_dev_threshold: float,
               seed: int):
  random.seed(seed)

  key_length_pairs = get_key_length_pairs(input_fasta_file)
  cluster_dict = cluster_by_std_dev(key_length_pairs, threshold=std_dev_threshold)
  best_sequences = select_best_sequences_from_clusters(cluster_dict)

  save_best_sequences(best_sequences, n_sequences_to_keep, \
                      input_fasta_file, output_fasta_file)
