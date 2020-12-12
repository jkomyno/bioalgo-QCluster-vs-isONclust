## Virtual Python env

- cd python
- python3 -m venv .venv
- source .venv/bin/activate
- pip install -r requirements.txt
- deactivate

## Preprocess Sequences

> Create a new Docker image called **clustering/preprocess** for preprocessing the Human genome

- `docker build -t clustering/preprocess -f Dockerfile.preprocess ./python/preprocess`

> Run the Docker image we've just created

- `./scripts/preprocess.sh`

## Simulate Sequences

> Create a new Docker image called **clustering/simlord** for simulating sequences

- `docker build -t clustering/simlord -f Dockerfile.simlord .empty`

> Run the Docker image we've just created

- `./scripts/simulate.sh`

## Cluster with isONclust

> Create a new Docker image called **clustering/isonclust** for clustering sequences

- `docker build -t clustering/isonclust -f Dockerfile.isonclust ./third-party`

> Run the Docker image we've just created

- `./scripts/isONclust.sh`

## Cluster with qCluster

> Create a new Docker image called **clustering/qcluster** for clustering sequences

- `docker build -t clustering/qcluster -f Dockerfile.qcluster .empty`

> Run the Docker image we've just created

- `./scripts/qCluster.sh`

## Compute cluster quality metrics

> Create a new Docker image called **clustering/quality** for computing the cluster quality metrics

- `docker build -t clustering/quality -f Dockerfile.quality ./python/quality`
