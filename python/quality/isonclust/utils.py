from os import path
from collections import defaultdict

from typing import Tuple, Dict, Set


def read_inferred_clusters(args) -> Tuple[Dict[str, int], Dict[int, Set[str]]]:
  tsv_file = path.join(args.data, 'isONclust', args.simulated,
                       args.result, 'final_clusters.tsv')

  clusters = defaultdict(dict)
  cluster_id_to_read_ids_map = defaultdict(set)

  with open(tsv_file, 'r') as f:
    for line in f:
      cluster_id, header = line.strip().split('\t')
      cluster_id = int(cluster_id)

      # e.g. 'm99726/100/CCS'
      read_id = header.split('_')[0]

      clusters[read_id] = cluster_id
      cluster_id_to_read_ids_map[cluster_id].add(read_id)

  return clusters, cluster_id_to_read_ids_map
