from dataclasses import dataclass, astuple


@dataclass(frozen=True)
class ExternalEvaluation:
  """
  External cluster validation consists in comparing the results of a cluster
  analysis to an externally known result (ground truth).
  It measures the extent to which cluster labels match externally supplies
  cluster labels.
  """

  # A clustering result is homogeneous if all of its clusters contain only
  # data points which are members of a single class.
  #
  # Range: [0, 1], where 1 is the perfect result.
  homogeneity: float

  # A clustering result is complete if all the data points that are members
  # of a given class are elements of the same cluster.
  #
  # Range: [0, 1], where 1 is the perfect result.
  completeness: float

  # Harmonic mean between homogeneity and completeness.
  #
  # Range: [0, 1], where 1 is the perfect result.
  v_measure: float

  # Range: [-1, 1], where 1 is the perfect result.
  adjusted_mutual_information: float

  # The Rand Index (RI) computes a similarity measure between two clustering
  # by considering all pairs of samples and counting pairs that are assigned in
  # the same or different clusters in the predicted and true clusterings.
  # The Adjusted Rand Index (ARI) is ensured to have a value close to 0.0 for
  # random labeling independently of the number of clusters and samples and
  # exactly 1.0 when the clusterings are identical.
  #
  # Range: [-1, 1], where 1 is the perfect result.
  adjusted_rand_index: float

  # The Fowlkes-Mallows index (FMI) is defined as the geometric mean between of
  # the precision and recall.
  #
  # Range: [0, 1], where 1 is the perfect result.
  fowlkes_mallows: float

  # To compute purity, each cluster is assigned to the class which is most
  # frequent in the cluster, and then the accuracy of this assignment is
  # measured by counting the number of correct assignments divided by the
  # cardinality of the cluster.
  #
  # Range: [0, 1], where 1 is the perfect result. 
  purity: float

  # Inverse of the purity score
  inverse_purity: float


  def __str__(self):
    return (f'\n\t- Homogeneity: {self.homogeneity}\n'
            f'\t- Completeness: {self.completeness}\n'
            f'\t- V-measure: {self.v_measure}\n'
            f'\t- Adjusted Mutual Information: {self.adjusted_mutual_information}\n'
            f'\t- Adjusted RI: {self.adjusted_rand_index}\n'
            f'\t- Fowlkes-Mallows: {self.fowlkes_mallows}\n'
            f'\t- Purity: {self.purity}\n'
            f'\t- Inverse purity: {self.inverse_purity}\n')


  def __iter__(self):
    """
    Enables iterating over data class fields
    """
    return iter(self.__dict__.items())
