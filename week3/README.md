# Week 3 – Introduction to MPI

## Overview

This week introduced **parallel programming using MPI (Message Passing Interface)**. The goal was to compare **serial and parallel implementations** of simple programs and evaluate performance when using multiple processes.

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

#### Timing (MPI Hello World)

| Processes | Real Time |
| --------- | --------- |
| 2         | ~0.42s    |
| 4         | ~0.43s    |
| 8         | ~0.44s    |
| 16        | ~0.48s    |

**Observation:**

* Runtime remains roughly constant regardless of process count
* MPI introduces significant startup overhead (~0.4s), dominating execution time for simple programs

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

* Internal computation time is reduced by distributing work across processes
* However, total runtime is dominated by MPI overhead at this scale
* For the input sizes tested, the serial version is faster overall

---

### 3. Performance Comparison

General behaviour observed:

* Increasing the number of processes increases total system work (user + sys time)
* Real runtime does not significantly decrease due to MPI startup and communication overhead
* Parallel execution is occurring, but does not provide a real-time speedup for small problem sizes

---

## 4. MPI Program Breakdown (`proof.c`)

The `proof.c` program demonstrates a basic MPI communication pattern using a **root-client model**.

### Structure

* The program initialises MPI and determines the **rank** and **number of processes**
* One process (rank 0) acts as the **root**
* All other processes act as **clients**

### Pseudocode

**main():**

* Check input arguments
* Initialise MPI
* Get rank and total number of processes
* Verify communicator size
* Call appropriate task (root or client)
* Finalise MPI

**check_task():**

* If rank == 0 → execute root task
* Else → execute client task

**client_task():**

* Compute value = rank × input argument
* Send value to root process using `MPI_Send`

**root_task():**

* Loop over all client processes
* Receive values using `MPI_Recv`
* Add received values to a running total
* Print final sum

### Behaviour

* Each client computes a partial result independently
* The root process collects and sums all results
* This demonstrates a simple **parallel reduction pattern** using point-to-point communication

---

## Conclusions

From the experiments:

* MPI enables parallel execution by distributing work across multiple processes
* Parallel programs reduce internal computation time, but overall runtime can be dominated by overhead
* For small workloads, serial implementations are faster due to the cost of process startup and communication
* Performance improvements from MPI depend on sufficiently large problem sizes
* Understanding the balance between computation and communication is essential for efficient parallel programming

Overall, MPI provides a powerful framework for parallel computation, but performance gains depend strongly on problem size and overhead costs.
