from dataclasses import dataclass, astuple
from typing import Union


@dataclass(frozen=True)
class ClusterStats:
  """
  Clusters stats gathers some statistics about the cluster composition,
  in particular about how the cluster cardinality varies.
  """

  # number of clusters
  k: int

  # minimum number of reads in a cluster
  min_size: Union[int, None]

  # maximum number of reads in a cluster
  max_size: Union[int, None]

  # average number of reads in a cluster
  avg_size: Union[float, None]

  # standard deviation in the number of reads in a cluster
  std_size: Union[float, None]


  def __str__(self):
    return (f'\n\t- k: {self.k}\n'
            f'\t- Minimum size: {self.min_size}\n'
            f'\t- Maximum size: {self.max_size}\n'
            f'\t- Average size: {self.avg_size}\n'
            f'\t- Standard deviation of size: {self.std_size}\n')


  def __iter__(self):
    """
    Enables iterating over data class fields
    """
    return iter(self.__dict__.items())
