from sklearn.metrics.cluster import homogeneity_completeness_v_measure
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import fowlkes_mallows_score
from typing import List

from . import ExternalEvaluation


def compute_external_metrics(labels_true: List[str], labels_pred: List[int]) -> ExternalEvaluation:
  homogeneity, completeness, v_measure = homogeneity_completeness_v_measure(labels_true, labels_pred)
  adjusted_rand_index = adjusted_rand_score(labels_true, labels_pred)
  fowlkes_mallows = fowlkes_mallows_score(labels_true, labels_pred)

  return ExternalEvaluation(homogeneity=homogeneity, completeness=completeness, v_measure=v_measure,
                            adjusted_rand_index=adjusted_rand_index, fowlkes_mallows=fowlkes_mallows)
