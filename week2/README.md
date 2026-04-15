# Week 2 – Performance and Parallelism

## Overview

This week focused on benchmarking and analysing the performance of programs using different timing methods. Experiments were carried out using both **C (compiled)** and **Python (interpreted)** implementations to compare execution time across a variety of tasks.

The `time` command was used to measure overall runtime (wall clock time), while internal timing methods were used to measure specific code sections. 

---

## Programs Included

* `hello_world.c / .py` – basic runtime comparison
* `repeat_adder.c / .py` – scaling behaviour of inefficient multiplication
* `time_print.c / .py` – internal timing of loops
* `write_file.c / .py` – file writing performance
* `read_file.c / .py` – file reading performance

---

## How to Compile and Run

### Compile (C)

```bash
gcc file.c -o ~/bin/file
```

### Run

```bash
# C
time ~/bin/file [args]

# Python
time python3 file.py [args]
```

---

## Results and Analysis

### 1. Hello World (C vs Python)

| Language | Real Time |
| -------- | --------- |
| Python   | ~0.033s   |
| C        | ~0.005s   |

**Observation:**
C executes significantly faster than Python. This reflects the difference between compiled (C) and interpreted (Python) execution.

---

### 2. Repeat Adder (Scaling Behaviour)

#### Python Results

| Input     | Output | Time    |
| --------- | ------ | ------- |
| 4, 5      | 20     | ~0.032s |
| 1000, 5   | 5000   | ~0.029s |
| 100000, 5 | 500000 | ~0.034s |
| 5, 100000 | 500000 | ~0.030s |
| 5, 10000  | 50000  | ~0.031s |

#### C Results

| Input     | Output | Time    |
| --------- | ------ | ------- |
| 1000, 5   | 5000   | ~0.006s |
| 100000, 5 | 500000 | ~0.004s |
| 5, 100000 | 500000 | ~0.003s |
| 5, 10000  | 50000  | ~0.004s |

**Observations:**

* C is consistently faster than Python for all inputs.
* Runtime depends primarily on the first argument (loop count).
* The second argument has negligible impact on runtime.
* Even with large inputs, execution time remains relatively small due to simple operations.

---

### 3. Internal Timing (time_print)

#### C Results (selected)

* 1,000 gives an internal runtime of approximately 0.00034 seconds
* 100,000 gives an external runtime of approximately 0.015 seconds

#### Python Results (selected)

* 1,000 gives an internal runtime of approximately 0.00056 seconds
* 100,000 gives an external runtime of approximately 0.081 seconds

**Observations:**

* Runtime increases with input size, showing expected scaling behaviour.
* Python is significantly slower than C, especially for larger inputs.
* Printing to the screen contributes significantly to runtime; redirecting output to `/dev/null` gives a better indication of computation time.

---

### 4. File I/O Performance

#### Python Results

| Size   | Write Time | Read Time |
| ------ | ---------- | --------- |
| 1,000  | ~0.004s    | ~0.0016s  |
| 5,000  | ~0.0066s   | ~0.0034s  |
| 10,000 | ~0.0090s   | ~0.0034s  |
| 50,000 | ~0.0244s   | ~0.0077s  |

#### C Results

| Size   | Write Time | Read Time |
| ------ | ---------- | --------- |
| 1,000  | ~0.00019s  | ~0.00029s |
| 5,000  | ~0.00062s  | ~0.00098s |
| 10,000 | ~0.00159s  | ~0.00185s |
| 50,000 | ~0.00708s  | ~0.00756s |

**Observations:**

* C is significantly faster for file writing operations.
* File reading times are more similar between C and Python.
* Runtime scales with file size in both languages.
* File I/O is slower than simple computation due to system-level operations.

---

## Conclusions

From all experiments conducted:

* C consistently outperforms Python across all tested tasks due to compilation into machine code.
* Python is easier to use but slower, particularly for computation-heavy loops.
* Runtime scales with workload size, especially in loop-based programs.
* File I/O operations are slower than computation and scale with data size.
* Choice of algorithm matters: inefficient methods such as repeat addition clearly demonstrate scaling behaviour.
* External timing using `time` measures total runtime, while internal timing isolates specific parts of code.

Overall, C is better suited for performance-critical applications, while Python offers flexibility and ease of use at the cost of speed.
