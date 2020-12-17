from os import path
from collections import defaultdict

from typing import Tuple, Dict, Set


def read_inferred_clusters(args) -> Tuple[Dict[str, int], Dict[int, Set[str]], int]:
  tsv_file = path.join(args.data, 'random_cluster', args.simulated,
                       args.result, 'inferred_clusters.tsv')

  clusters = defaultdict(dict)
  cluster_id_to_read_ids_map = defaultdict(set)
  k = set()

  with open(tsv_file, 'r') as f:
    for line in f:
      cluster_id, read_id = line.strip().split('\t')
      cluster_id = int(cluster_id)

      clusters[read_id] = cluster_id
      cluster_id_to_read_ids_map[cluster_id].add(read_id)
      k.add(cluster_id)

  return clusters, cluster_id_to_read_ids_map, len(k)
