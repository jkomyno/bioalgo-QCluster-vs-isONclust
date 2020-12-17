## Experiment

1. Extract 100 chromosomes from data/original/input.fasta and save it into preprocess/preprocessed.fasta
2. Create 6 synthetic datasets. 10000, 20000, 50000 reads are simulated starting from the 100 selected chromosomes. The reads length is either 100 or 700.
3. Run qCluster with grid parameters
4. Run isONclust with grid parameters
5. Collect cluster metrics for each clustering result
6. Analyze clusters performance

**TODO**: We should log the time needed to execute qCluster and isONclust in a logfile called 'time.log'.

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

## Generate baseline random clustering

> Create a new Docker image called **clustering/random_cluster** for clustering sequences randomly

- `docker build -t clustering/random_cluster -f Dockerfile.random_cluster ./python/random_cluster`

> Run the Docker image we've just created

- `./scripts/random_cluster.sh`
