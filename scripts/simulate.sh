#!/bin/bash

docker run \
  -v "$(pwd)/data":/data \
  -v "$(pwd)/python/simulate":/usr/app/simulate \
  clustering/simlord /data
