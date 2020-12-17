import argparse
from . import random_cluster


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--data', type=str, help='Location of the data folder')
  parser.add_argument('--simulated', type=str, help='Name of the simulated dataset')
  parser.add_argument('-k', type=int, help='Number of clusters to generate')
  args = parser.parse_args()

  print(f'Args:\n{args}\n')

  seed = 42
  random_cluster(args, seed)
