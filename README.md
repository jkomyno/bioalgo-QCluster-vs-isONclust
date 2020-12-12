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
