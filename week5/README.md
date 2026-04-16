# Week 5 – Communicators and Topologies

## Overview

This week focused on modelling oscillations on a string and then parallelising that model with MPI. The work progressed from an original serial program, to an improved serial version, to MPI implementations using different communication topologies.

The main aims were:

* to understand the structure of the serial string model
* to remove hard-coding and improve usability
* to parallelise the simulation with MPI
* to compare a linear topology with a ring topology
* to evaluate whether this problem benefits from parallel execution

---

## Programs Included

* `string_wave.c` – original serial implementation
* `string_wave_v2.c` – improved serial implementation with command-line arguments
* `string_wave_mpi.c` – MPI implementation using a linear topology
* `string_wave_mpi_ring.c` – MPI implementation using a ring topology
* `animate_line_file.py` – animation script with input/output arguments
* `animate_line_file_v2.py` – more modular animation script

---

## How to Compile and Run

### Part 1 – Serial String Wave

```bash
gcc HPQC/week5/string_wave.c -o ~/bin/string_wave -lm
./bin/string_wave 50
python3 HPQC/week5/animate_line_file.py data/string_wave.csv serial.gif
```

### Improved Serial Version

```bash
gcc HPQC/week5/string_wave_v2.c -o ~/bin/string_wave_v2 -lm
./bin/string_wave_v2 <points> <cycles> <samples> <output_file>
```

### Part 2 – MPI String Wave (Linear Topology)

```bash
mpicc HPQC/week5/string_wave_mpi.c -o ~/bin/string_wave_mpi -lm
time mpirun -np <processes> ~/bin/string_wave_mpi 48 5 25 <output_file>
python3 HPQC/week5/animate_line_file.py <output_file> linear.gif
```

Tested with 1, 2, and 4 processes.

### Part 3 – MPI String Wave (Ring Topology)

```bash
mpicc HPQC/week5/string_wave_mpi_ring.c -o ~/bin/string_wave_mpi_ring -lm
time mpirun -np <processes> ~/bin/string_wave_mpi_ring 48 5 25 <output_file>
python3 HPQC/week5/animate_line_file.py <output_file> ring.gif
```

Tested with 1, 2, and 4 processes.

---

## Part 1 – Serial Code

### Original Serial Version

The original `string_wave.c` program simulates a simple wave on a string using hard-coded parameters for cycles, samples, and output location.

At each time step:

* the first point is driven by a sine function
* each subsequent point takes the value of its left neighbour
* all positions are written to a CSV file

This produces a travelling wave moving from left to right.

---

### Improvements in `string_wave_v2.c`

The improved version removes hard-coded values and introduces a modular structure.

Key improvements:

* command-line arguments for `points`, `cycles`, `samples`, and output file
* flexible file handling instead of fixed output path
* clearer structure using functions:

  * `check_args()`
  * `initialise_vector()`
  * `generate_timestamps()`
  * `update_positions()`
  * `print_header()`

This makes the code easier to read, reuse, and extend for MPI.

---

### Serial Model Behaviour

The simulation:

1. generates timestamps
2. initialises positions to zero
3. applies a sinusoidal driver at the first point
4. shifts values along the string

This creates a clear travelling wave suitable for visualisation.

---

## Part 2 – MPI Parallel Simulation (Linear Topology)

### Domain Decomposition

The string is split across processes:

```c
local_n = points / size;
```

Each process updates its own section.

---

### Communication and Aggregation

* neighbouring processes exchange boundary values
* rank 0 applies the driving force
* `MPI_Gather` collects all data on rank 0
* only rank 0 writes to the output file

---

### Performance (Linear)

| Processes | Real Time |
| --------- | --------- |
| 1         | ~0.41 s   |
| 2         | ~0.47 s   |
| 4         | ~0.44 s   |

No meaningful speedup was observed because communication overhead dominated computation.

---

## Part 3 – Ring Topology

### Topology Change

The neighbour structure becomes:

```c
int left  = (rank - 1 + size) % size;
int right = (rank + 1) % size;
```

This creates **periodic boundary conditions**, connecting the ends of the domain.

---

### Communication

* implemented using `MPI_Sendrecv`
* all processes communicate every timestep
* no special boundary cases are required

---

### Behaviour

* linear topology: the wave travels across the domain
* ring topology: the wave wraps around continuously

Despite this, the animations appear very similar because the update rule only depends on the left neighbour.

---

### Performance (Ring)

| Processes | Real Time |
| --------- | --------- |
| 1         | ~0.40 s   |
| 2         | ~0.53 s   |
| 4         | ~0.47 s   |

Again, no performance gain was observed because communication cost outweighed the computational benefit.

---

## Visualisation

### Serial

<div align="center">
<img width="640" height="480" alt="animate_string_file" src="https://github.com/user-attachments/assets/9f2e1ec7-b27c-4124-870b-44cd50128ed1" />
</div>

### MPI Linear Topology

<div align="center">
<img width="640" height="480" alt="mpi_output" src="https://github.com/user-attachments/assets/b71ef2a3-81c5-4ec9-b156-3611ade0e735" />
</div>

### MPI Ring Topology

<div align="center">
<img width="640" height="480" alt="ring" src="https://github.com/user-attachments/assets/f3fd1a5a-19b1-4516-83c6-f08545f4a765" />
</div>

The serial and MPI outputs are visually very similar, confirming that the parallel implementations preserve the behaviour of the original model. The ring topology adds periodic boundary conditions without significantly changing the observed wave pattern for this simple update rule.

---

## Conclusions

* the serial model successfully simulates wave propagation
* `string_wave_v2.c` improves structure and usability
* the MPI implementations correctly reproduce the expected behaviour
* no speedup was observed for the tested problem size because communication overhead dominates
* the ring topology introduces periodic boundaries
* communication cost is a key factor in deciding whether parallelisation is worthwhile

This exercise showed that parallelisation must be matched carefully to both problem size and communication requirements.
