#!/bin/bash

docker run \
  -v "$(pwd)/data":/data \
  -v "$(pwd)/python":/usr/app/python \
  clustering/qcluster \
  /data
