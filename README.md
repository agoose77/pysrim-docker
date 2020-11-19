# pysrim-docker
[![pypi-badge][]][pypi] 

[pypi-badge]: https://img.shields.io/pypi/v/pysrim-docker
[pypi]: https://pypi.org/project/pysrim-docker

Docker executor for PySRIM

## Getting Started
To use this package, simply replace your `SR` or `TRIM` imports with those from `srim.docker`, e.g.
```python

from srim.docker import TRIM

trim = TRIM(...)
```

Out of the box, `pysrim-docker` uses the `costrouc/srim` Docker image, and writes the input and output files to a temporary directory. 

## How Does it Work?
`pysrim-docker` overrides the `run()` method of the `SR` and `TRIM` classes with one that executes a bash script in a particular Docker image.
This script simply copies the inputs to the appropriate directory, runs the required binary, and returns the results.

## Why?
Since using Docker, I have seen its utility in hiding obscure build steps behind a simple container image. 
However, I prefer to write code that might be part of an analysis pipeline, rather than standalone Python modules, and so it is prefereable to 
have the input file generation peformed on the host. An additional benefit of this is that the `pysrim` installation can be updated indepently of the Docker image.
