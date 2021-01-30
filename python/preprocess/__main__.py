import sys
from . import preprocess


if __name__ == '__main__':
  ####################
  #  Read arguments  #
  ####################

  input_fasta_file = sys.argv[1]
  output_fasta_file = sys.argv[2]
  n_sequences_to_keep = int(sys.argv[3])

  std_dev_threshold = 0.005
  seed = 42

  #####################
  #  Print arguments  #
  #####################

  print(f'input_fasta_file: {input_fasta_file}')
  print(f'output_fasta_file: {output_fasta_file}')
  print(f'n_sequences_to_keep: {n_sequences_to_keep}')
  print(f'std_dev_threshold: {std_dev_threshold}')
  print(f'seed: {seed}')
  print('')

  #######################
  #  Actual processing  #
  #######################

  preprocess(input_fasta_file, output_fasta_file, \
             n_sequences_to_keep, std_dev_threshold, \
             seed)
