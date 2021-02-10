# A Comparison of QCluster and isONclust for Clustering Synthetic Sequences

-------------------------------------------------------------------------

This project has been written in partial fulfillment of the requirements for the Algorithms for Bioinformatics class, supervised by [Professor Matteo Comin](http://www.dei.unipd.it/~ciompin).

## Abstract

In this project, we examine and compare two open-source software tools for the task of clustering short-read sequences according to their gene family of origin: [QCluster](https://github.com/CominLab/QCluster) and [isONclust](https://github.com/ksahlin/isONclust). We perform our analysis on six synthetic datasets simulated using `100` sequences selected from the human cDNA assembly `GRCh38.p13`. These datasets have `10000`,`20000`, and `50000` synthetic sequences, with two different fixed read depths (100bp and 700bp) and uniform simulated read errors. The purpose of our experiment is to evaluate how well QCluster and isONclust are able to cluster the simulated sequences with respect to the original `100` human cDNA sequences. We repeat our experiments using several configurations offered by the two software tools. We assess the quality of the clustering results using multiple external validation metrics, like *V-Measure* and *Adjusted Mutual Information*, and we empirically determine the interactions between the configuration parameters of the software using plot visualizations. Moreover, we compare the clustering results with theoutcome of a random baseline clustering method.

## Deliverables

A comprehensive report of the project can be found in [report.pdf](report.pdf).

To visualize the clustering quality plots and tables generated for this report, please refer to the [analysis.ipynb](analysis.ipynb) `Python` notebook.
If Github struggles to load the notebook file, please try viewing the notebook with [nbviewer](https://nbviewer.jupyter.org/github/jkomyno/bioalgo-QCluster-vs-isONclust/blob/master/analysis.ipynb).

We developed some modules written in Python3 to perform our experiments:

- `python/isonclust`: the module responsible for executing isONclust on all datasets with multiple configurations, saving the results
- `python/parameter_grid`: a data structure to lazily iterate over parameter configurations
- `python/preprocess`: the module used to select and save 100 sequences from the human cDNA assembly
- `python/cluster`: the module responsible for executing QCluster on all datasets with multiple configurations, saving the results
- `python/quality`: the module used to assess quality metrics and statistics on the clustering results, saving the insights
- `python/random_cluster`: the module responsible for performing a random clustering to be used as a baseline for our experiments
- `python/simulate`: the module used for creating the six simulated datasets with fixed read lengthsand uniform simulated read error distributions

## Clustering Quality Metrics

Since we only have access to the final outcome of `QCluster` and `isONclust` and not to the internally computed distances between the elements of the clusters, we cannot use internal evaluation methods for our experiments. Instead, we adopt the following external evaluation scores:

- Homogeneity
- Completeness
- V-Measure
- Adjusted Mutual Information *(AMI)*
- Adjusted Rand Index *(ARI)*

## Script Execution

#### Requirements

- Internet connection
- This repository: `git clone --recurse-submodules https://github.com/jkomyno/bioalgo-QCluster-vs-isONclust`
- Docker `v20.x.x`
- Any OS with Bash shell (for Windows, please use either [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install-win10) or install [Git Bash](https://gitforwindows.org))

If you want to download the original cDNA assembly we used to generate the simulated datasets, please refer to `Section 4` of the report for the instructions on how to download it (`~400`MB).

#### Processessing Sequences

The steps to preprocess the human cDNA sequences as described in `Section 4.1` of the report are:

- Create the `clustering/preprocess` Docker image with the command: 

```
  docker build -t clustering/preprocess \
      -f Dockerfile.preprocess ./python/preprocess
```

- Run the `clustering/preprocess` Docker image:

```
  ./scripts/preprocess.sh
```

The Python module in [`python/preprocess`](python/preprocess) will be run under the hood.
The file `data/preprocess/preprocessed.fasta` will be overwritten.

#### Simulating Datasets

The steps to create the simulated datasets as described in `Section 4.2` of the report are:

- Create the `clustering/simlord` Docker image with the command: 

```
  docker build -t clustering/simlord -f Dockerfile.simlord .empty
```

- Run the `clustering/simlord` Docker image:

```
  ./scripts/simulate.sh
```

The Python module in [`python/simulate`](python/simulate) will be run under the hood.
The folders in `data/simulated` will be overwritten.

#### Perform Baseline Clustering

The steps to perform baseline clustering on all datasets as described in `Section 5.2` of the report are:

- Create the `clustering/random_cluster` Docker image with the command: 

```
  docker build -t clustering/random_cluster \
      -f Dockerfile.random_cluster ./python/random_cluster
```

- Run the `clustering/random_cluster` Docker image:

```
  ./scripts/random_cluster.sh
```

The Python module in [`python/random_cluster`](python/random_cluster) will be run under the hood.
The folders in `data/random_cluster` will be overwritten.


#### Perform Clustering with QCluster

The steps to perform clustering with QCluster on all datasets as described in `Section 5.3` of the report are:

- Create the `clustering/qcluster` Docker image with the command: 

```
  docker build -t clustering/qcluster -f Dockerfile.qcluster .empty
```

- Run the `clustering/qcluster` Docker image:

```
  ./scripts/qCluster.sh
```

The Python module in [`python/qCluster`](python/qCluster) will be run under the hood.
The folders in `data/qCluster` will be overwritten.


#### Perform Clustering with isONclust

The steps to perform clustering with isONclust on all datasets as described in `Section 5.4` of the report are:

- Create the `clustering/isonclust` Docker image with the command: 

```
  docker build -t clustering/isonclust \
    -f Dockerfile.isonclust ./third-party
```

- Run the `clustering/isonclust` Docker image:

```
  ./scripts/isONclust.sh
```

The Python module in [`python/isONclust`](python/isONclust) will be run under the hood.
The folders in `data/isONclust` will be overwritten.


#### Compute Clustering Metrics

The steps to compute the clustering metrics and statistics on all clustering results as described in `Section 5.5` of the report are:

- Create the `clustering/quality` Docker image with the command: 

```
  docker build -t clustering/quality \
      -f Dockerfile.quality ./python/quality
```

- Run the `clustering/quality` Docker image:

```
  ./scripts/quality.sh
```

The Python module in [`python/quality`](python/quality) will be run under the hood.
The folders in `data/quality` will be overwritten.

## Citing

If you use this project for your research, please cite the following two papers.

`QCluster`:

```
  @article{Comin2015,
    doi = {10.1186/s13015-014-0029-x},
    url = {https://doi.org/10.1186/s13015-014-0029-x},
    year = {2015},
    month = jan,
    publisher = {Springer Science and Business Media {LLC}},
    volume = {10},
    number = {1},
    author = {Matteo Comin and Andrea Leoni and Michele Schimd},
    title = {Clustering of reads with alignment-free measures and quality values},
    journal = {Algorithms for Molecular Biology}
  }
```

`isONclust`:

```
  @incollection{Sahlin2019,
    doi = {10.1007/978-3-030-17083-7_14},
    url = {https://doi.org/10.1007/978-3-030-17083-7_14},
    year = {2019},
    publisher = {Springer International Publishing},
    pages = {227--242},
    author = {Kristoffer Sahlin and Paul Medvedev},
    title = {De Novo Clustering of Long-Read Transcriptome Data Using a Greedy,  Quality-Value Based Algorithm},
    booktitle = {Lecture Notes in Computer Science}
  }
```

## Acknowledgement

I thank Professor **Matteo Comin** ([Google Scholar](https://scholar.google.com/citations?user=HXG7EpYAAAAJ&hl=en), [Github](https://github.com/CominLab)) from the Department of Information Engineering of the University of Padova for his patient assistance and guidance for this project.

I would also like to thank Assistant Professor **Kristoffer Sahlin** ([Google Scholar](https://scholar.google.com/citations?user=IAGyYNEAAAAJ&hl=en), [Github](https://github.com/ksahlin)) from the Department of Mathematics at Stockholm University for his helpful support about our questions and doubts on the {\isonclust} software.

## License

[MIT License](LICENSE).
