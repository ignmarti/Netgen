# README #

This README DOCUMENTS THE FILES IN THIS REPOSITORY

### What is this repository for? ###

This repository contains pyhon code scripts to generate random traffic matrices, solve ILP or heuristic planning using Net2Plan and parse the files into a CSV
### How do I get set up? ###

Just need python, Net2Plan in parent directory and two folders to be pased as tmp folders for n2p files.

To run there are three scripts:

python generate_matrix.py NUM_MATRICES PATH_OUT -> Reads canonical.n2p and substitues its demands by a random number (or sums random noise)
python N2PSolveMulti.py INPUT OUTPUT -> solves Traffic Matrices defined in the n2p files in INPUT and stores resutls in OUTPUT
python parallelParse.py INPUT OUTPUT_FILE -> Reads n2p files and transforms them into a CSV where each entry represents a MT-solution pair
