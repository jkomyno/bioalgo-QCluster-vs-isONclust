import numpy as np
from sklearn.metrics.cluster import homogeneity_completeness_v_measure
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import fowlkes_mallows_score
from sklearn.metrics.cluster import contingency_matrix
from typing import List

from . import ExternalEvaluation


def compute_external_metrics(labels_true: List[str], labels_pred: List[int]) -> ExternalEvaluation:  
  if len(labels_true) == 0 and len(labels_pred) == 0:
    return None
  
  homogeneity, completeness, v_measure = homogeneity_completeness_v_measure(labels_true, labels_pred)
  adjusted_mutual_info = adjusted_mutual_info_score(labels_true, labels_pred)
  adjusted_rand_index = adjusted_rand_score(labels_true, labels_pred)
  fowlkes_mallows = fowlkes_mallows_score(labels_true, labels_pred)

  mat = contingency_matrix(labels_true, labels_pred)
  purity = purity_score(mat)
  inverse_purity = purity_score(mat, inverse=True)

  return ExternalEvaluation(homogeneity=homogeneity, completeness=completeness, v_measure=v_measure,
                            adjusted_mutual_information=adjusted_mutual_info, adjusted_rand_index=adjusted_rand_index,
                            fowlkes_mallows=fowlkes_mallows, purity=purity, inverse_purity=inverse_purity)


def purity_score(mat, inverse=False):
  """
  Compute purity or inverse purity score.
  """

  axis = 0 if inverse else 1
  return np.sum(np.amax(mat, axis=axis)) / np.sum(mat)
