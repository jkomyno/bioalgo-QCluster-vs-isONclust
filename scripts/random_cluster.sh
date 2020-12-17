#!/bin/bash

for filename in ./data/simulated/n-*; do
  [ -e "$filename" ] || continue
  DATASET=$(basename ${filename})

  echo "dataset: ${DATASET}"
  echo ""

  docker run \
    -v "$(pwd)/data":/data \
    -v "$(pwd)/python/random_cluster":/usr/app/random_cluster \
    clustering/random_cluster \
    --data /data \
    --simulated ${DATASET} \
    -k 100
done
