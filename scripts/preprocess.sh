#!/bin/bash

docker run \
  -v "$(pwd)/data":/data \
  -v "$(pwd)/python/preprocess":/usr/app/preprocess \
  clustering/preprocess \
  /data/original/input.fasta \
  /data/preprocess/preprocessed.fasta \
  100
