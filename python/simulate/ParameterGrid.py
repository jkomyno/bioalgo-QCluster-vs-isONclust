from itertools import product

class ParameterGrid:
  """
  Grid of parameters with a discrete number of values for each.
  Can be used to iterate over parameter value combinations.
  """

  def __init__(self, param_grid):
    self.param_grid = param_grid

  def __iter__(self):
    """
    Iterate over the points in the grid.
    """
    # sort keys of a dictionary for reproducibility
    items = sorted(self.param_grid.items())
    if not items:
      yield {}
    else:
      keys, values = zip(*items)
      # for each entry v of the cartesian product
      for v in product(*values):
        params = dict(zip(keys, v))
        yield params
