from typing import Dict, Tuple, List, Set


def compute_cluster_labels(clusters: Dict[str, int], 
                           classes: Dict[str, str],
                           without: Set[int] = set()) -> Tuple[List[str], List[int]]:
  labels_true, labels_pred = zip(*[
    (classes[read_id], clusters[read_id])
    for read_id in clusters
    if clusters[read_id] not in without
  ])

  return labels_true, labels_pred
