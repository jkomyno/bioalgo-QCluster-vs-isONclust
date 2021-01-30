import sys

from . import isONclust

if __name__ == '__main__':
  ####################
  #  Read arguments  #
  ####################

  data_folder = sys.argv[1]

  #####################
  #  Print arguments  #
  #####################

  print(f'data_folder: {data_folder}')
  print('')

  #######################
  #  Actual Simulating  #
  #######################

  isONclust(data_folder)
