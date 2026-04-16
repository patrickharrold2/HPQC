# Week 4 – MPI Communications

## Overview

This week focused on communication in MPI programs. The work covered:

* basic point-to-point communication
* refactoring communication code into clearer functions
* comparing different send variants
* measuring latency and bandwidth with ping-pong tests
* comparing manual communication with collective operations

The aim was not just to make the programs run, but to compare how different communication strategies behave and how much overhead they introduce.

---

## Programs Included

* `comm_test_mpi.c` – original point-to-point communication example
* `comm_test_mpi_v2.c` – refactored version with separate functions
* `comm_test_mpi_v3_*` – send variants (`send`, `ssend`, `bsend`, `rsend`, `isend`)
* `pingpong.c` – latency benchmark
* `pingpong_bandwidth.c` – bandwidth benchmark
* `vector_mpi_baseline.c` – baseline vector summation comparison
* `vector_mpi_bcast.c` – broadcast-based version
* `vector_mpi_scatter.c` – scatter-based version
* `vector_mpi_collect.c` – send/recv, gather, and reduce comparison
* `vector_mpi_custom_reduce.c` – custom reduction operation

---

## How to Compile and Run

### Compile

```bash
# Communication tests
mpicc HPQC/week4/comm_test_mpi_*.c -o ~/bin/

# Ping-pong tests
mpicc HPQC/week4/pingpong_*.c -o ~/bin/

# Collective tests
mpicc HPQC/week4/vector_mpi_*.c -o ~/bin/
```

where * is one of the variants

### Run

#### Communication tests (example with 4 processes)

```bash
mpirun -np 4 ~/bin/comm_test_mpi
mpirun -np 4 ~/bin/comm_test_mpi_v2
mpirun -np 4 ~/bin/comm_test_mpi_v3_<variant>
```

Where `<variant>` is one of: `send`, `ssend`, `bsend`, `rsend`, `isend`.

#### Ping-pong tests

```bash
mpirun -np 2 ~/bin/pingpong <pings>
mpirun -np 2 ~/bin/pingpong_bandwidth <pings> <bytes>
```

#### Collective tests

```bash
mpirun -np 4 ~/bin/vector_mpi_<method> 1000
```

Where `<method>` includes: `baseline`, `bcast`, `scatter`, `collect`, `custom_reduce`.

---

## Part 1 – Demonstrating Communications

### Step 1 – Original `comm_test_mpi.c`

The program demonstrates basic point-to-point communication. Non-root ranks send values to rank 0, which receives and prints them.

* Output order is non-deterministic due to independent process execution
* All values are received correctly

Timed run (4 processes):

* real ≈ 0.416 s
* user ≈ 0.098 s
* sys ≈ 0.193 s

---

### Step 2 – Refactoring into Functions

The program was refactored into:

* `root_task()` – handles receives
* `client_task()` – handles sends
* `check_task()` – assigns roles
* `check_uni_size()` – validates process count

This improves readability and extensibility.

---

### Step 3–4 – Send Variants and Benchmarking

Tested variants:

* `MPI_Send`, `MPI_Ssend`, `MPI_Bsend`, `MPI_Rsend`, `MPI_Isend`

**Observations:**

* All variants worked correctly
* Timings are extremely small (microseconds)
* Variation between runs is comparable to the measured values
* `MPI_Ssend` appears slightly more consistent
* `MPI_Send` is the most practical general-purpose choice

---

## Part 2 – Latency and Bandwidth

### Latency Results

| Pings | Avg time per ping-pong (s) |
| ----- | -------------------------- |
| 10    | 0.000005                   |
| 100   | 0.000002                   |
| 1000  | 0.000001                   |
| 10000 | 0.000001                   |

Latency converges to approximately **1 µs**.

---

### Bandwidth Results

| Size (bytes) | Avg time (s) |
| ------------ | ------------ |
| 8            | 0.000001     |
| 64           | 0.000001     |
| 512          | 0.000002     |
| 4096         | 0.000009     |
| 32768        | 0.000016     |
| 262144       | 0.000079     |
| 1048576      | 0.000259     |

---

### Bandwidth Plots

<div align="center">
<img src="https://github.com/user-attachments/assets/b08fbd69-26ea-411a-ab45-4c834027dec1" width="650">
</div>

<div align="center">
<img src="https://github.com/user-attachments/assets/a54e1407-6a3e-4a4e-9dce-f06854b1aee4" width="650">
</div>

The linear plot shows overall scaling, while the log-scale plot highlights behaviour across small and large message sizes.

* Small messages are latency-dominated
* Larger messages show approximately linear scaling

---

### Derived Performance

From linear fit:

* slope ≈ 2.44 × 10⁻¹⁰ s/byte
* intercept ≈ 5.39 × 10⁻⁶ s

Derived:

* bandwidth ≈ **4.1 GB/s**
* latency ≈ **5 µs** (fit)

Direct measurement gives ≈ **1 µs latency**, with the higher fitted value caused by noise at small sizes.

---

## Part 3 – Collective Communications

### Broadcast vs Scatter vs DIY

| Method  | Runtime (s)     |
| ------- | --------------- |
| DIY     | 0.00008–0.00014 |
| Scatter | 0.000119        |
| Bcast   | 0.000188        |

For small inputs, avoiding communication is fastest.

---

### Send/Recv vs Gather vs Reduce

| Method    | Runtime (s) |
| --------- | ----------- |
| Send/Recv | 0.000134    |
| Gather    | 0.000163    |
| Reduce    | 0.000254    |

Manual methods outperform collectives at small scale due to overhead.

---

### Custom Reduce

| Input  | Runtime (s) |
| ------ | ----------- |
| 1000   | 0.000125    |
| 10000  | 0.000245    |
| 100000 | 0.000586    |

Matches built-in reduction behaviour and scales with input size.

---

## Conclusions

* MPI communication overhead dominates small workloads
* Send variant differences are negligible at this scale
* Latency ≈ 1 µs, bandwidth ≈ 4 GB/s
* Collective methods are not always optimal for small inputs
* Communication strategy must match problem size

MPI communication is efficient at scale, but overhead must always be considered.
