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
* `comm_test_mpi_v3_send.c` – version using `MPI_Send`
* `comm_test_mpi_v3_ssend.c` – version using `MPI_Ssend`
* `comm_test_mpi_v3_bsend.c` – version using `MPI_Bsend`
* `comm_test_mpi_v3_rsend.c` – version using `MPI_Rsend`
* `comm_test_mpi_v3_isend.c` – version using `MPI_Isend`
* `pingpong.c` – latency benchmark
* `pingpong_bandwidth.c` – bandwidth benchmark
* `vector_mpi_baseline.c` – baseline vector summation comparison
* `vector_mpi_bcast.c` – broadcast-based version
* `vector_mpi_scatter.c` – scatter-based version
* `vector_mpi_collect.c` – send/recv, gather, and reduce comparison
* `vector_mpi_custom_reduce.c` – custom reduction operation
* `bandwidth_results.csv` – recorded bandwidth test data

---

## How to Compile and Run

### Part 1 – Communication Tests

```bash
mpicc HPQC/week4/comm_test_mpi.c -o ~/bin/comm_test_mpi
mpicc HPQC/week4/comm_test_mpi_v2.c -o ~/bin/comm_test_mpi_v2

mpicc HPQC/week4/comm_test_mpi_v3_send.c  -o ~/bin/comm_test_mpi_v3_send
mpicc HPQC/week4/comm_test_mpi_v3_ssend.c -o ~/bin/comm_test_mpi_v3_ssend
mpicc HPQC/week4/comm_test_mpi_v3_bsend.c -o ~/bin/comm_test_mpi_v3_bsend
mpicc HPQC/week4/comm_test_mpi_v3_rsend.c -o ~/bin/comm_test_mpi_v3_rsend
mpicc HPQC/week4/comm_test_mpi_v3_isend.c -o ~/bin/comm_test_mpi_v3_isend

mpirun -np 4 ~/bin/comm_test_mpi
mpirun -np 4 ~/bin/comm_test_mpi_v2
mpirun -np 4 ~/bin/comm_test_mpi_v3_send
mpirun -np 4 ~/bin/comm_test_mpi_v3_ssend
mpirun -np 4 ~/bin/comm_test_mpi_v3_bsend
mpirun -np 4 ~/bin/comm_test_mpi_v3_rsend
mpirun -np 4 ~/bin/comm_test_mpi_v3_isend
```

### Part 2 – Ping-Pong Latency and Bandwidth

```bash
mpicc HPQC/week4/pingpong.c -o ~/bin/pingpong
mpicc HPQC/week4/pingpong_bandwidth.c -o ~/bin/pingpong_bandwidth

mpirun -np 2 ~/bin/pingpong 10
mpirun -np 2 ~/bin/pingpong 100
mpirun -np 2 ~/bin/pingpong 1000
mpirun -np 2 ~/bin/pingpong 10000

mpirun -np 2 ~/bin/pingpong_bandwidth 10000 8
mpirun -np 2 ~/bin/pingpong_bandwidth 10000 64
mpirun -np 2 ~/bin/pingpong_bandwidth 10000 512
mpirun -np 2 ~/bin/pingpong_bandwidth 10000 4096
mpirun -np 2 ~/bin/pingpong_bandwidth 10000 32768
mpirun -np 2 ~/bin/pingpong_bandwidth 10000 262144
mpirun -np 2 ~/bin/pingpong_bandwidth 10000 1048576
```

### Part 3 – Collective Communication Tests

```bash
mpicc HPQC/week4/vector_mpi_baseline.c -o ~/bin/vector_mpi_baseline
mpicc HPQC/week4/vector_mpi_bcast.c -o ~/bin/vector_mpi_bcast
mpicc HPQC/week4/vector_mpi_scatter.c -o ~/bin/vector_mpi_scatter
mpicc HPQC/week4/vector_mpi_collect.c -o ~/bin/vector_mpi_collect
mpicc HPQC/week4/vector_mpi_custom_reduce.c -o ~/bin/vector_mpi_custom_reduce

mpirun -np 4 ~/bin/vector_mpi_baseline 1000
mpirun -np 4 ~/bin/vector_mpi_bcast 1000
mpirun -np 4 ~/bin/vector_mpi_scatter 1000

mpirun -np 4 ~/bin/vector_mpi_collect 1000 sendrecv
mpirun -np 4 ~/bin/vector_mpi_collect 1000 gather
mpirun -np 4 ~/bin/vector_mpi_collect 1000 reduce

mpirun -np 4 ~/bin/vector_mpi_custom_reduce 1000
mpirun -np 4 ~/bin/vector_mpi_custom_reduce 10000
mpirun -np 4 ~/bin/vector_mpi_custom_reduce 100000
```

Compile and run commands match the command record you assembled. 

---

## Part 1 – Demonstrating Communications

### Step 1 – Original `comm_test_mpi.c`

The original communication program demonstrated basic point-to-point communication. Non-root ranks sent a value to rank 0, and rank 0 received and printed the messages.

Example behaviour with 4 processes:

* rank 1 sent 10
* rank 2 sent 20
* rank 3 sent 30
* rank 0 received all values correctly

The key observation was that the order of the printed messages was not deterministic. This is normal in MPI because processes execute independently and communication timing varies slightly between runs. 

A timed run with 4 processes gave:

* real time ≈ 0.416 s
* user time ≈ 0.098 s
* sys time ≈ 0.193 s 

### Step 2 – Refactoring into Functions

The original `comm_test_mpi.c` kept its logic inside `main()`, which made it harder to follow and harder to extend. In the refactored version, `comm_test_mpi_v2.c`, the logic was split into dedicated functions:

* `root_task()` handles receiving messages
* `client_task()` handles sending messages
* `check_task()` assigns work based on rank
* `check_uni_size()` validates that enough processes are available

This made the program easier to read, easier to test, and much easier to extend into the send-variant versions used later.

### Step 3 – Send Variants

The code was then modified to explicitly test:

* `MPI_Send`
* `MPI_Ssend`
* `MPI_Bsend`
* `MPI_Rsend`
* `MPI_Isend`

All variants completed successfully in the recorded tests. The main difference was not correctness but behaviour and timing. Output order still varied, and the timings were extremely small.

Before testing, I expected `MPI_Ssend` to be more predictable because it is synchronous, and `MPI_Isend` to be less predictable because it is non-blocking. I also expected that the measured timings would fluctuate enough that it would be difficult to rank the methods cleanly for such a small message size.

That is broadly what happened. `MPI_Ssend` appeared more consistent, while the other methods showed small but noisy differences. For this task, ordinary `MPI_Send` was the most practical choice because it was simple and reliable.

### Step 4 – Benchmarking the Send Variants

Internal timing was added around the send and receive calls. Measured times were all on the order of microseconds.

Summary of timed behaviour for 4 processes:

| Variant     | General behaviour                                   |
| ----------- | --------------------------------------------------- |
| `MPI_Send`  | reliable, simple, small timings                     |
| `MPI_Ssend` | more synchronous, slightly more consistent          |
| `MPI_Bsend` | also worked correctly, similar scale timings        |
| `MPI_Rsend` | worked here, but depends on receiver readiness      |
| `MPI_Isend` | non-blocking behaviour, timing also highly variable |

The main conclusion was that the variance in timings was comparable to the timings themselves, exactly as expected for such short communication events.

---

## Part 2 – Benchmarking Latency and Bandwidth

### How `pingpong.c` Works

`pingpong.c` must be run with exactly 2 processes. Rank 0 starts a timer using `MPI_Wtime()`, then repeatedly sends an integer counter to rank 1. Rank 1 receives it, increments it, and sends it back. This repeats until the counter reaches the requested number of ping-pong exchanges. Rank 0 then prints:

* final counter
* elapsed time
* average time per ping-pong

This matches the intended ping-pong logic from the brief. 

### Latency Results

| Pings | Final Counter | Elapsed (s) | Average per ping-pong (s) |
| ----- | ------------: | ----------: | ------------------------: |
| 10    |            10 |    0.000050 |                  0.000005 |
| 100   |           100 |    0.000242 |                  0.000002 |
| 1000  |          1000 |    0.001075 |                  0.000001 |
| 10000 |         10000 |    0.008734 |                  0.000001 |

As the number of pings increased, the average time converged to about **1 microsecond per ping-pong**. This gave a reasonable estimate of the communication latency on the system. 

### How `pingpong_bandwidth.c` Works

The bandwidth version extends the ping-pong test by sending an **array** instead of a single integer. It:

* takes `num_pings` and `num_bytes` as arguments
* converts requested byte count into a number of `int` elements
* allocates an array with `malloc()`
* stores the counter in `data[0]`
* sends the full array back and forth between the two ranks
* times the total communication in the same way as the latency version

This makes it possible to study how runtime changes with message size.

### Bandwidth Results

| Message Size | Elapsed (s) | Average per ping-pong (s) |
| ------------ | ----------: | ------------------------: |
| 8 B          |    0.010584 |                  0.000001 |
| 64 B         |    0.009793 |                  0.000001 |
| 512 B        |    0.015360 |                  0.000002 |
| 4096 B       |    0.088129 |                  0.000009 |
| 32768 B      |    0.159770 |                  0.000016 |
| 262144 B     |    0.785587 |                  0.000079 |
| 1048576 B    |    2.589125 |                  0.000259 |

For very small messages, latency dominates. Once messages become larger, elapsed time grows roughly linearly with size. From the organised results, the data suggests an effective bandwidth in the order of **hundreds of MB/s, around 400 MB/s**, with a baseline latency around **1 µs**.

---

## Part 3 – Collective Communications

These exercises reused the vector summation idea from Week 3 and compared manual communication with collective MPI operations.

### Step 1 – Broadcast vs Scatter vs DIY

The tested methods were:

* **Baseline / DIY**: each process independently builds its own copy of the data
* **Broadcast**: root builds the array and sends the whole thing to everyone
* **Scatter**: root builds the array and distributes chunks

Before testing, I expected `MPI_Scatter` to perform best overall because it sends only the data each process needs, while `MPI_Bcast` sends the entire array to all processes. I expected the DIY version to waste memory, but for small inputs it might still be competitive because it avoids communication overhead.

Results for `n = 1000` with 4 processes:

| Method         |    Sum | Internal runtime (s) |
| -------------- | -----: | -------------------: |
| Baseline / DIY | 500500 |    0.000080–0.000137 |
| `MPI_Bcast`    | 500500 |             0.000188 |
| `MPI_Scatter`  | 500500 |             0.000119 |

For this small input, the DIY baseline was fastest, followed by scatter, then broadcast. This suggests that for small problems the communication overhead can outweigh the cost of rebuilding the same data redundantly on each process.

### Step 2 – Send/Recv vs Gather vs Reduce

In `vector_mpi_collect.c`, rank 0 creates the full vector and `MPI_Scatter` distributes chunks to all processes. Each process computes a local sum. Then the program switches mode based on the second command-line argument:

* `sendrecv`: non-root ranks send local sums to rank 0, which receives them in a loop and accumulates the total
* `gather`: all local sums are gathered on rank 0 with `MPI_Gather`, then rank 0 adds them up
* `reduce`: `MPI_Reduce` combines local sums directly into a global sum on rank 0

Before testing, I expected `MPI_Reduce` to be the fastest in principle because it is designed specifically for reduction operations, followed by `MPI_Gather`, with manual send/recv the least elegant. For small inputs, though, I expected overheads to blur the difference.

Results for `n = 1000` with 4 processes:

| Method       |    Sum | Internal runtime (s) |
| ------------ | -----: | -------------------: |
| Send/Recv    | 500500 |             0.000134 |
| `MPI_Gather` | 500500 |             0.000163 |
| `MPI_Reduce` | 500500 |             0.000254 |

For this test size, manual send/recv was fastest and reduce was slowest. This was likely due to fixed overheads dominating at small scale. For larger workloads, collective operations would be expected to scale better and become more worthwhile.

### Step 3 – Custom Reduce Operation

A custom reduction operation was implemented and tested.

Results:

| Input (n) |       Sum | Internal runtime (s) |
| --------- | --------: | -------------------: |
| 1000      |    500500 |             0.000125 |
| 10000     |  50005000 |             0.000245 |
| 100000    | 705082704 |             0.000586 |

The custom reduce produced correct results relative to the integer representation being used and scaled with input size. Performance was comparable to the built-in reduction approach. At `n = 100000`, the result again showed integer overflow, matching the behaviour already seen in Week 3. 

---

## Conclusions

This week showed that MPI communication is strongly shaped by overhead.

For small messages and small workloads:

* startup costs and fixed communication costs dominate
* timing differences between send variants are noisy
* manual methods can outperform collective methods

From the latency test, the system latency was approximately **1 µs**. From the bandwidth test, effective bandwidth was on the order of **hundreds of MB/s**. For collective operations, the most theoretically elegant method was not always the fastest at small scale.

The main lessons were:

* communication order in MPI is often non-deterministic
* refactoring into functions makes communication code much easier to extend
* small timing measurements must be interpreted cautiously because variance is high
* collective operations are useful, but their benefits depend on problem size
* benchmarking should always accompany design decisions rather than relying only on intuition

Overall, this week demonstrated that communication strategy is just as important as computation strategy in parallel programming.
