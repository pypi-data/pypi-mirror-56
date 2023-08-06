# Pyaesar
Pyaesar: A Multi-Noded Multi-Processor API

## License
This software is licensed under the [BSD 3-Clause License](http://opensource.org/licenses/BSD-3-Clause). Please see below for the license.

## About Pyaesar
This Software Package allows users to take advantage of multi-processing on multiple nodes.
This code is developed as a combination of the [multi-process API](https://docs.python.org/3/library/multiprocessing.html)
and the [MPI4Py API](https://mpi4py.readthedocs.io/en/stable/) (similar to a MAP).
By leveraging the MPI4Py code we can distribute the data across nodes and then generate a
pool on each node to process the data concurrently.

``Pyaesar`` is a combination of MPI4Py and Python Multiprocess. This software package
allows users to take advantage of multi-processing on multiple nodes.

``multiprocess`` is a package from the Python language which supports the spawning of processes
using the standard library. ``multiprocess`` has been distributed in the standard
library since Python 2.6.

Features:

* An ``Emperor `` class makes it easy to submit tasks to a pool of worker
  processes.

* The ``Emperor`` class allows you to distribute the tasks to a set of pools that can be distributed across nodes

* Allows for the distribution on Embarrassingly Parallel code processing across Nodes

Any user feedback, bug reports, comments, or suggestions are highly appreciated.

## Requirements
Software:

* Pre-requisite: MPI
* Python module: multiprocess
* Python Module: MPI4Py

Program:
* 1 Process per Node
  * mpirun -N 1 python name-of-file.py


## To Note
Certain implementations of MPI do not support `fork()`, which the `multiprocess` library uses to spawn processes on Unix systems.
If `fork()` is not supported, the MPI runtime will  print a warning like the following:
```
--------------------------------------------------------------------------
A process has executed an operation involving a call to the
"fork()" system call to create a child process.  Open MPI is currently
operating in a condition that could result in memory corruption or
other system errors; your job may hang, crash, or produce silent
data corruption.  The use of fork() (or system() or other calls that
create child processes) is strongly discouraged.

The process that invoked fork was:

  Local host:          [[4727,3],2] (PID 23933)

If you are *absolutely sure* that your application will successfully
and correctly survive a call to fork(), you may disable this warning
by setting the mpi_warn_on_fork MCA parameter to 0.
--------------------------------------------------------------------------
```
If you encounter this error, you can avoid using `multiprocess` by creating an Emperor with only one process:
```py
import Pyaesar.Emperor as Emperor

Em = Emperor(nproc=1)
...
```
In this case, you may also launch more than one rank per node to increase the parallelism,
although this method is not generally recommended due to the overhead of additional MPI ranks.


For more information about the `fork()` warning, see the following:

- https://www.open-mpi.org/faq/?category=tuning#fork-warning
- https://www.open-mpi.org/faq/?category=openfabrics#ofa-fork


## Install / Uninstall

`Pyaesar` requires an MPI compiler to install. Ensure that that your system has a valid MPI installation before attempting to install `Pyaesar`.

### Pip

We've added `Pyaesar` to the [Python Package Index](https://pypi.org/project/Pyaesar/). To install `Pyaesar` with `pip` simply run
```sh
pip install Pyaesar
```

To uninstall `Pyaesar` simply run
```sh
pip uninstall Pyaesar
```

### From source

Follow these steps to install `Pyaesar` from source.

1. Clone this repository
```sh
git clone git@gitlab.com:jamilggafur/pyaesar.git
```

2. Install `Pyaesar` using setuptools

```sh
cd pyaesar
python3 setup.py install
```

3. If you're contributing to `Pyaesar`, we recommend using the development build

```sh
cd pyaesar
python3 setup.py develop
```

To uninstall `Pyaesar` simply run
```sh
pip uninstall Pyaesar
```

## How to use
* This code is designed to work in the following format:
  * Node: Rank 0: breaks up the data in multiple sections that are about equally distributable between the set of nodes
  * Using MPI4Py, each section of data is distributed its associated node
  * Creates a Multiprocess pool on each node and processes the code

In order to accomplish this you need to ha
* In order
* Python Module: MPI4Py

## Newest Version
You can get the latest development version with all the shiny new features at::
    https://gitlab.com/jamilggafur/pyaesar

If you have a new contribution, please submit a pull request.


## More Information
The best way to get started is to look at the documentation, and the examples in the Examples folder.
There we have three examples of how to use the Pyaesar API.

Please feel free to submit a ticket on GitLab.  If you would like to share how you use
``Pyaesar`` in your work, please send an email
(to **jamilgafur @ gmail dot com**).


## Citation
If you use ``Pyaesar`` to do research that leads to publication, we ask that you
acknowledge use of ``Pyaesar`` by citing the following in your publication::

```
@MISC{Pyaesar_2018,
  author       = {Jamil Gafur and David {Neill Asanza} and Geoffrey Fairchild and Carrie Manore},
  title        = {{Pyaesar: A Multi-Noded Multi-Processor API}},
  month        = Sep,
  year         = 2019,
  version      = {1.0.3},
  journal      = {GitLab repository},
  howpublished = {\url{https://gitlab.com/jamilggafur/pyaesar/}},
}
```

## License
copyright 2019. Triad National Security, LLC.
All rights reserved.

This program was produced under U.S. Government contract 89233218CNA000001 for Los Alamos National Laboratory (LANL), which is operated by Triad National Security, LLC for the U.S. Department of Energy/National Nuclear Security Administration. All rights in the program are reserved by Triad National Security, LLC, and the U.S. Department of Energy/National Nuclear Security Administration. The Government is granted for itself and others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide license in this material to reproduce, prepare derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so.




This program is open source under the BSD-3 License.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

