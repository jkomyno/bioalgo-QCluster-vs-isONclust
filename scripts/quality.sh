#!/bin/bash

set -e

DATA=./data
THRESHOLD=5

function generate_quality_csv {
  TOOL=$1

  echo "tool: ${TOOL}"
  echo ""

  for filename in $DATA/$TOOL/n-*/*-*/; do
    [ -e "$filename" ] || continue
    DATASET=$(basename $(dirname ${filename}))
    CLUSTERING=$(basename ${filename})

    echo "dataset: ${DATASET}"
    echo "clustering parameters: ${CLUSTERING}"
    echo ""

    docker run \
      -v "$(pwd)/data":/data \
      -v "$(pwd)/python/quality":/usr/app/quality \
      clustering/quality \
      --data /data \
      --simulated ${DATASET} \
      --result ${CLUSTERING} \
      --threshold ${THRESHOLD} \
      $TOOL

    echo ""
  done
}

echo "trivial threshold: ${THRESHOLD}"

generate_quality_csv 'qCluster';
generate_quality_csv 'isONclust';

for filename in ./data/simulated/n-*; do
  [ -e "$filename" ] || continue
  DATASET=$(basename ${filename})
  echo "dataset: ${DATASET}"

  docker run \
    -v "$(pwd)/data":/data \
    -v "$(pwd)/python/quality":/usr/app/quality \
    clustering/quality \
    --data /data \
    --simulated ${DATASET} \
    --result "" \
    --threshold ${THRESHOLD} \
    "random_cluster"
done
