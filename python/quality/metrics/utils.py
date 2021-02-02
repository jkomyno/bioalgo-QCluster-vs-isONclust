import numpy as np
from operator import itemgetter
from . import ClusterStats
from typing import Dict, Tuple, List, Set


def compute_cluster_labels(clusters: Dict[str, int], 
                           classes: Dict[str, str],
                           without: Set[int] = set()) -> Tuple[List[str], List[int]]:
  lst = [
    read_id for read_id in clusters
    if clusters[read_id] not in without
  ]

  if len(lst) == 0:
      return [], []

  class_cluster_pair_list = [
    (classes[read_id], clusters[read_id])
    for read_id in lst
  ]

  labels_true = list(map(itemgetter(0), class_cluster_pair_list))
  labels_pred = list(map(itemgetter(1), class_cluster_pair_list))

  return labels_true, labels_pred


def compute_cluster_stats(k: int, cluster_id_to_read_ids_map: Dict[int, Set[str]]) -> ClusterStats:
  cardinalities = list(map(len, cluster_id_to_read_ids_map.values()))

  if len(cardinalities) > 0:
    min_size = min(cardinalities)
    max_size = max(cardinalities)
    avg_size = np.mean(cardinalities)
    std_size = np.std(cardinalities)
  else:
    min_size = None
    max_size = None
    avg_size = None
    std_size = None

  return ClusterStats(k=k, min_size=min_size, max_size=max_size,
                      avg_size=avg_size, std_size=std_size)
