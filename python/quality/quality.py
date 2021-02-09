import pandas as pd
from os import path
from pathlib import Path
from pysam import AlignmentFile
from collections import defaultdict
from typing import Dict, Set, Tuple, Iterator

from . import isonclust
from . import qcluster
from . import random_cluster
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
  args.tool:         'isONclust' | 'qCluster' | 'random_cluster'
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
  
  tool = args.tool

  """
  clusters = {
    'm99998/100/CCS': 234,
    'm99999/100/CCS': 102,
    ...
  }
  """

  if tool == 'isONclust':
    clusters, cluster_id_to_read_ids_map, k = isonclust.read_inferred_clusters(args)
  elif tool == 'qCluster':
    clusters, cluster_id_to_read_ids_map, k = qcluster.read_inferred_clusters(args)
  elif tool == 'random_cluster':
    clusters, cluster_id_to_read_ids_map, k = random_cluster.read_inferred_clusters(args)

  cluster_stats = metrics.compute_cluster_stats(k, cluster_id_to_read_ids_map)
  print(f'cluster_stats:{cluster_stats}')

  trivial_class_chromosomes = set(compute_trivial_classes(chromosome_to_read_ids_map, threshold=args.threshold))
  print(f'# trivial classes: {len(trivial_class_chromosomes)}')
  assert len(trivial_class_chromosomes) == 0

  labels_true, labels_pred = metrics.compute_cluster_labels(clusters, classes)
  external_evaluation = metrics.compute_external_metrics(labels_true, labels_pred)
  print(f'External evaluation: {external_evaluation}\n')

  if external_evaluation is not None:
    df = create_quality_dataframe(external_evaluation=external_evaluation,
                                  cluster_stats=cluster_stats)
    write_quality_dataframe_to_csv(df, args)

  if tool == 'random_cluster':
    return
  
  # metrics for singleton clusters
  singleton_cluster_ids = set(compute_trivial_clusters(cluster_id_to_read_ids_map, threshold=1))
  print(f'# singleton clusters: {len(singleton_cluster_ids)}')
  labels_true_no_singleton, labels_pred_no_singleton = metrics.compute_cluster_labels(clusters, classes, without=singleton_cluster_ids)
  external_evaluation_no_singleton = metrics.compute_external_metrics(labels_true_no_singleton, labels_pred_no_singleton)
  print(f'External evaluation (no singleton): {external_evaluation_no_singleton}\n')

  if external_evaluation_no_singleton is not None:
      df = create_quality_dataframe(external_evaluation=external_evaluation_no_singleton, 
                                    cluster_stats=cluster_stats)
      write_quality_dataframe_to_csv(df, args, prefix='no_singleton_')

  # metrics for trivial clusters wrt `args.threshold`
  trivial_cluster_ids = set(compute_trivial_clusters(cluster_id_to_read_ids_map, threshold=args.threshold))
  print(f'# trivial clusters: {len(trivial_cluster_ids)}')
  labels_true_no_trivial, labels_pred_no_trivial = metrics.compute_cluster_labels(clusters, classes, without=trivial_cluster_ids)
  external_evaluation_no_trivial = metrics.compute_external_metrics(labels_true_no_trivial, labels_pred_no_trivial)
  print(f'External evaluation (no trivial): {external_evaluation_no_trivial}\n')

  if external_evaluation_no_trivial is not None:
    df = create_quality_dataframe(external_evaluation=external_evaluation_no_trivial, 
                                  cluster_stats=cluster_stats)
    write_quality_dataframe_to_csv(df, args, prefix='no_trivial_')

  # number of clusters by quality types
  n_clusters = k
  n_clusters_trivial = len(trivial_cluster_ids)
  n_clusters_singleton = len(singleton_cluster_ids)

  df = create_n_clusters_dataframe(n_clusters, n_clusters_trivial, n_clusters_singleton)
  write_n_clusters_dataframe_to_csv(df, args)


def create_n_clusters_dataframe(n_clusters: int,
                                n_clusters_trivial: int,
                                n_clusters_singleton: int) -> pd.DataFrame:
  data = {
    'k': [n_clusters],
    'k_non_trivial': [n_clusters - n_clusters_trivial],
    'k_trivial': [n_clusters_trivial],
    'k_singleton': [n_clusters_singleton],
  }
  df = pd.DataFrame.from_dict(data)
  return df


def write_n_clusters_dataframe_to_csv(df: pd.DataFrame, args):
  csv_filename = f'{args.result}_n_clusters.csv'
  csv_path = path.join(args.data, 'quality', args.tool, args.simulated)
  Path(csv_path).mkdir(parents=True, exist_ok=True)

  df.to_csv(path.join(csv_path, csv_filename), sep=',', index=False,
          encoding='utf-8', decimal='.')


def write_quality_dataframe_to_csv(df: pd.DataFrame, args, prefix: str = ''):
  csv_prefix = f'{prefix}{args.result}'

  if len(csv_prefix) > 0:
    csv_prefix = f'{csv_prefix}_'

  csv_filename = f'{csv_prefix}quality.csv'
  csv_path = path.join(args.data, 'quality', args.tool, args.simulated)
  Path(csv_path).mkdir(parents=True, exist_ok=True)

  df.to_csv(path.join(csv_path, csv_filename), sep=',', index=False,
            encoding='utf-8', decimal='.')


def create_quality_dataframe(external_evaluation: metrics.ExternalEvaluation,
                             cluster_stats: metrics.ClusterStats) -> pd.DataFrame:
  metrics_data = {
    metric_name: [metric_value] for (metric_name, metric_value) in external_evaluation
  }

  cluster_stats_data = {
    stat_name: [stat_value] for (stat_name, stat_value) in cluster_stats
  }

  data = {
    **metrics_data,
    **cluster_stats_data,
  }

  df = pd.DataFrame.from_dict(data)
  return df
