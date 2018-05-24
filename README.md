# NETgen: A Network data generation tool #

Netgen application is a python Wrapper built over [Net2Plan](http://www.net2plan.com/) to generate/label network data related to optimization problems in network settings. The system consists in three different components that work on separate python files and run during three phases in the data generation process.

### Requirements ###

This code is optimized for python 3 and requires the following python modules:

* numpy
* xml

Additionally, there must be a working copy of Net2Plan in your computer with the CPLEX ILP solver installled

### Installation ###

To install this code, just download the repository and modify the first line of the *solve.cfg* file to point to the Net2Plan folder.

### Running modules ###

The system is separated in three modules with three different functions: Data generation, Data labeling and Result compression.


#### Data Generation ####

Randomly generate Traffic matrices modified from a *canonical* network topology and traffic matrix generated in Net2Plan. Takes as input an *n2p* file and generates as many matrices as desired. The traffic generation process is based on adding random noise to the original Traffic matrix

```python generate_matrix.py NUM_MATRICES PATH_OUT [VARIABILITY] [THREAD_POOL] [CANONICAL_FILE] [MULTIPLICITY_FACTOR] [MODE]```

Where each of the parameters represent:

* *NUM_MATRICES*: The number of matrices to generate
* *PATH_OUT*: The folder where resulting Net2Plan files will be stored
* *CANONICAL_FILE*: The Net2Plan file describing network topology and initial traffic matrix (That would be modified)
* *VARIABILITY*: The percentage of variability with respect to mean value to apply. *Default value:0.1*
* *MULTIPLICITY_FACTOR*: The amount by which the traffic entries will be modified. *Default value: 1*
* *MODE*: The random distribution to be used. *Supported Modes: GAUSSIAN, UNIFORM*. *Default value:GAUSSIAN*
* *THREAD_POOL*: Number of processes to be span, according to computer resources. *Default value: 5*



-> Reads canonical.n2p and substitues its demands by a random number (or sums random noise)
python N2PSolveMulti.py INPUT OUTPUT -> solves Traffic Matrices defined in the n2p files in INPUT and stores resutls in OUTPUT
python parallelParse.py INPUT OUTPUT_FILE -> Reads n2p files and transforms them into a CSV where each entry represents a MT-solution pair
