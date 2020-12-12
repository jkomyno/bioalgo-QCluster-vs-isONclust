from os import path
from pysam import AlignmentFile
from collections import defaultdict
from typing import Dict, Set, Tuple, Iterator

from . import isonclust
from . import qcluster
from . import metrics


def parse_true_clusters(args) -> Tuple[Dict[str, str], Dict[str, Set[str]]]:
  ground_truth_filename = path.join(args.data, 'simulated', args.simulated, 'simulated.sam')
  # reference_filename = path.join(args.data, 'preprocess', 'preprocessed.fasta')

  ref_file = AlignmentFile(ground_truth_filename, mode='r', check_sq=True)
  # reference_filename=reference_filename)

  classes = defaultdict(dict)
  chromosome_to_read_ids_map = defaultdict(set)

  for read in ref_file.fetch(until_eof=True):
    header = read.query_name
    # e.g. 'm96770/100/CCS'
    read_id = header.split(' ')[0]
    
    # e.g. 'ENSG00000070061|ENSG00000070061.16|ENST00000674938|ENST00000674938.1'
    chromosome = header.split(';')[3].split('=')[1]

    classes[read_id] = chromosome
    chromosome_to_read_ids_map[chromosome].add(read_id)

  return classes, chromosome_to_read_ids_map


def compute_trivial_classes(chromosome_to_read_ids_map: Dict[str, Set[str]],
                            threshold: int) -> Iterator[str]:
  """
  A class is considered trivial if a chromosome has been used to generate
  at most `threshold` sequences.
  """

  for chromosome in chromosome_to_read_ids_map:
    read_ids = chromosome_to_read_ids_map[chromosome]
    l = len(read_ids)
    if l <= threshold:
      yield chromosome


def compute_trivial_clusters(cluster_id_to_read_ids_map: Dict[int, Set[str]],
                             threshold: int) -> Iterator[str]:
  """
  A cluster is considered trivial if it contains at most `threshold` sequences.
  """

  for cluster_id in cluster_id_to_read_ids_map:
    read_ids = cluster_id_to_read_ids_map[cluster_id]
    l = len(read_ids)
    if l <= threshold:
      yield cluster_id


def quality(args):
  """
  args.data:         Location of the data folder
  args.simulated:    Name of the simulated dataset
  args.result:       Location of the cluster result
  args.threshold:    Clusters which contain at most `threshold` sequences are considered trivial
  args.is_isonclust: True iff the quality of isONclust must be evaluated
  args.is_qcluster:  True iff the quality of qCluster must be evaluated
  """
  
  """
  {
    'm99998/100/CCS': 'ENSG00000100150|ENSG00000100150.20|ENST00000646515|ENST00000646515.1',
    'm99999/100/CCS': 'ENSG00000187866|ENSG00000187866.10|ENST00000394264|ENST00000394264.7'
  }
  """
  classes, chromosome_to_read_ids_map = parse_true_clusters(args)

  # by simulation we know classes of all reads, they are therefore the same number
  tot_nr_reads = len(classes)

  if hasattr(args, 'is_isonclust'):
    """
    {
      'm77337/100/CCS': 6410,
      'm82581/100/CCS': 6411
    }
    """
    clusters, cluster_id_to_read_ids_map = isonclust.read_inferred_clusters(args)
  elif hasattr(args, 'is_qcluster'):
    """
    {
      'm99998/100/CCS': 234,
      'm99999/100/CCS': 102
    }
    """
    clusters, cluster_id_to_read_ids_map = qcluster.read_inferred_clusters(args)

  trivial_class_chromosomes = set(compute_trivial_classes(chromosome_to_read_ids_map, threshold=args.threshold))
  print(f'# trivial classes: {len(trivial_class_chromosomes)}')

  singleton_cluster_ids = set(compute_trivial_clusters(cluster_id_to_read_ids_map, threshold=1))
  print(f'# singleton clusters: {len(singleton_cluster_ids)}')

  trivial_cluster_ids = set(compute_trivial_clusters(cluster_id_to_read_ids_map, threshold=args.threshold))
  print(f'# trivial clusters: {len(trivial_cluster_ids)}')

  labels_true, labels_pred                           = metrics.compute_cluster_labels(clusters, classes)
  labels_true_no_singleton, labels_pred_no_singleton = metrics.compute_cluster_labels(clusters, classes, without=singleton_cluster_ids)
  labels_true_no_trivial, labels_pred_no_trivial     = metrics.compute_cluster_labels(clusters, classes, without=trivial_cluster_ids)

  external_evaluation              = metrics.compute_external_metrics(labels_true, labels_pred)
  external_evaluation_no_singleton = metrics.compute_external_metrics(labels_true_no_singleton, labels_pred_no_singleton)
  external_evaluation_no_trivial   = metrics.compute_external_metrics(labels_true_no_trivial, labels_pred_no_trivial)

  print(f'External evaluation: {external_evaluation}\n')
  print(f'External evaluation (no singleton): {external_evaluation_no_singleton}\n')
  print(f'External evaluation (no trivial): {external_evaluation_no_trivial}\n')
