import argparse
from . import quality


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  qcluster_parser = subparsers.add_parser('qCluster', help='Evaluate the quality of qCluster')
  qcluster_parser.set_defaults(is_qcluster=True)

  isonclust_parser = subparsers.add_parser('isONclust', help='Evaluate the quality of isONclust')
  isonclust_parser.set_defaults(is_isonclust=True)

  parser.add_argument('--data', type=str, help='Location of the data folder')
  parser.add_argument('--simulated', type=str, help='Name of the simulated dataset')
  parser.add_argument('--result', type=str, help='Location of the cluster result')
  parser.add_argument('--threshold', type=int, const=10, help='Clusters which contain at most `threshold` sequences are considered trivial')
  args = parser.parse_args()

  print(f'Args:\n{args}\n')

  quality(args)
