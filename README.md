# HPQC – High Performance and Quantum Computing Portfolio

This repository contains my practical portfolio for the **PHY1090 High Performance and Quantum Computing** module.

## Structure

The repository is organised into sub-directories of each of the classical computing exercises by week, as well as one for the quantum computing tutorial:

* `week2/` – Performance and benchmarking (C vs Python, timing, file I/O)
* `week3/` – Introduction to MPI (Hello World, vector addition, serial vs parallel)
* `week4/` – MPI communications (send types, latency, bandwidth, collectives)
* `week5/` – Parallel simulation (string oscillation model)
* `quantum/` – Quantum computing exercises (qubit operations, gates, and simulations)

Each folder contains the relevant source code and a `README.md` explaining:

* what each program does
* how to compile and run it
* what results were obtained and conclusions drawn
* notes on exercises where no code implementation was required

## Requirements

Code was developed and tested on the DCU HPC cluster (Cheetah) using:

* `gcc` and `mpicc`
* `mpirun`
* `python3` (used for benchmarking, file I/O, visualisation, and quantum exercises)

Some programs require linking with the math library:

```bash
-lm
```

## Running the Code

General workflow:

```bash
# Compile
gcc file.c -o output
mpicc file.c -o output

# Run
./output [args]
mpirun -np <processes> ./output [args]
```

See individual folders for exact commands and examples.

## Notes

* Binary files are not included in this repository
* Output data files are generated at runtime where required
* Results and analysis are documented in each folder's README

---

This repository is submitted as part of the PHY1090 Practical Portfolio.

