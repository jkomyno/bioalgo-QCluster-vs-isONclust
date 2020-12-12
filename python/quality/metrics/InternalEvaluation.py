from dataclasses import dataclass, astuple


@dataclass(frozen=True)
class InternalEvaluation:
  """
  Internal cluster validation uses the internal information of the clustering
  process to evaluate the goodness of a clustering structure without reference
  to external information.
  """

  # The Davies-Bouldin score is defined as the average similarity measure of
  # each cluster with its most similar cluster, where similarity is the ratio
  # of within-cluster distances to between-cluster distances.
  # Thus, clusters which are farther apart and less dispersed will result in
  # a better score.
  #
  # Range: [0, +∞], where 0 is the perfect result.
  davies_bouldin: float

  # Silhouette analysis measures how well an observation is clustered and it
  # estimates the average distance between clusters.
  #
  # Range: [-∞, 1], where 1 is the perfect result. 
  silhouette: float

  def __iter__(self):
    """
    Enables iterating over data class fields
    """
    return iter(astuple(self))
