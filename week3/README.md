# Week 3 – Introduction to MPI

## Overview

This week introduced **parallel programming using MPI (Message Passing Interface)**. The goal was to compare **serial and parallel implementations** of simple programs and evaluate performance improvements when using multiple processes.

Experiments focused on:

* understanding MPI structure (`MPI_Init`, `MPI_Comm_rank`, `MPI_Finalize`)
* comparing serial vs parallel execution
* analysing performance and scalability

---

## Programs Included

* `hello_serial.c` – basic serial hello world
* `hello_mpi.c` – parallel hello world using MPI
* `vector_serial.c` – serial vector summation
* `vector_mpi.c` – parallel vector summation using MPI

---

## How to Compile and Run

### Compile

```bash
gcc hello_serial.c -o hello_serial
gcc vector_serial.c -o vector_serial

mpicc hello_mpi.c -o hello_mpi
mpicc vector_mpi.c -o vector_mpi
```

### Run

```bash
# Serial
./hello_serial
./vector_serial [size]

# MPI
mpirun -np <processes> ./hello_mpi
mpirun -np <processes> ./vector_mpi [size]
```

---

## Results and Analysis

### 1. Hello World (Serial vs MPI)

**Serial Output:**

* Single process prints one message

**MPI Output:**

* Each process prints its own message with rank

**Observations:**

* MPI creates multiple independent processes
* Each process identifies itself using its rank
* Output order is not guaranteed due to parallel execution

---

### 2. Vector Addition (Serial vs MPI)

#### Serial

* Entire computation performed by a single process
* Runtime increases linearly with vector size

#### MPI

* Work is divided between processes
* Each process computes a portion of the vector
* Results are combined at the end

**Observations:**

* Parallel version reduces computation time for larger inputs
* Overhead exists due to communication between processes
* For small inputs, parallel version may be slower than serial

---

### 3. Performance Comparison

General behaviour observed:

* Increasing the number of processes reduces runtime for large inputs
* Speedup is not perfectly linear due to communication overhead
* Efficiency decreases as the number of processes increases beyond optimal levels

---

## Conclusions

From the experiments:

* MPI enables parallel execution by distributing work across multiple processes
* Parallel programs can significantly outperform serial versions for large workloads
* Communication overhead limits performance gains, especially for small tasks
* Optimal performance depends on balancing computation and communication costs
* Understanding workload distribution is key to efficient parallel programming

Overall, MPI provides a powerful framework for parallel computation, but performance gains depend on problem size and implementation efficiency.
