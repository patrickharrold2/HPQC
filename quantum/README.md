# Quantum – ENCCS Quantum Computing for Beginners Tutorial Work

## Overview

This folder contains my work based on the ENCCS **Quantum Computing for Beginners** tutorial series by Martin N. P. Nilsson. The series is split into three parts:

* **Part 1** – building a simple quantum computer simulator as a stack machine using Python and NumPy
* **Part 2** – extending the simulator to implement **Grover’s search**
* **Part 3** – adapting the simulator to use **PyTorch** so the workspace can run on either CPU or GPU ([ENCCS][1])

My work follows that same progression:

* a NumPy-based simulator with qubit stack operations and gate application
* an extended version adding Grover-style search logic
* a PyTorch-based version adapted for CPU/GPU execution

---

## Files Included

* `part1_*.py` – NumPy-based simulator following the Part 1 tutorial
* `part2_*.py` – Grover-search extension based on the Part 2 tutorial
* `part3_*.py` – PyTorch version based on the Part 3 GPU tutorial

The exact filenames in this folder may differ slightly, but they correspond to those three stages of development.

---

## Tutorial Context

### Part 1 – Quantum Computer as a Stack Machine

The first ENCCS tutorial introduces a simple way to simulate a quantum computer using:

* a **workspace** representing the state vector
* a **name stack** for qubit ordering
* NumPy functions such as `reshape`, `kron`, `matmul`, `swapaxes`, `linalg.norm`, and `random.choice` ([ENCCS][1])

This is the basis of my first script.

### Part 2 – Grover’s Search

The second tutorial extends the simulator to implement **Grover’s search**, showing how phase oracles and repeated amplitude amplification can be built on top of the basic simulator. It also gives the standard formula for the number of Grover iterations,

$$
k=\left\lfloor \frac{\pi}{4}\sqrt{M}-\frac{1}{2}\right\rfloor
$$

for a search space of size (M). ([ENCCS][2])

This is the basis of my second script.

### Part 3 – GPU/CPU Simulation with PyTorch

The third tutorial replaces NumPy operations with **PyTorch** so that the simulator can run with tensors on CPU or GPU. The central idea is that the quantum workspace lives in PyTorch memory and operations are performed there directly. ([ENCCS][3])

This is the basis of my third script.

---

## Part 1 – Basic Quantum Simulator

The first script implements the main features introduced in Part 1 of the ENCCS tutorial:

* `pushQubit(name, weights)`
  Adds a qubit to the simulator state, normalises the amplitudes, and expands the workspace using a Kronecker product.

* `tosQubit(name)`
  Moves a chosen qubit to the top of the stack so that gates can be applied in the correct order.

* `applyGate(gate, *names)`
  Applies a gate matrix to one or more selected qubits.

* `probQubit(name)`
  Calculates measurement probabilities for a chosen qubit.

* `measureQubit(name)`
  Measures a qubit probabilistically and collapses the state.

* predefined gates such as:

  * `X_gate`
  * `Y_gate`
  * `Z_gate`
  * `H_gate`
  * `S_gate`
  * `T_gate`
  * `CNOT_gate`
  * `CZ_gate`
  * `SWAP_gate`
  * `TOFF_gate`

This follows the tutorial’s core idea of treating the simulator as a stack-based quantum workspace. ([ENCCS][1])

### Part 1 Test

The script includes a final test based on a **Toffoli-equivalent gate sequence**, where qubits `Q1`, `Q2`, and `Q3` are prepared and measured repeatedly. The purpose of this test is to demonstrate that multi-qubit gate behaviour can be composed from simpler gates.

---

## Part 2 – Grover’s Search Extension

The second script extends the simulator to implement a basic version of **Grover’s search**, matching the focus of the ENCCS Part 2 tutorial. ([ENCCS][2])

### Main Additions

* `zero_booleanOracle(qubits, result)`
  Marks the all-zero state using a Boolean-style oracle.

* `zero_phaseOracle(qubits)`
  Applies a phase flip to the all-zero state.

* `sample_phaseOracle(qubits)`
  Implements a sample oracle for the chosen marked state.

* `groverSearch(n, printProb=True)`
  Carries out the Grover iterations:

  1. initialise all qubits in superposition
  2. apply the phase oracle
  3. apply Hadamard gates
  4. apply the zero-state phase oracle
  5. apply Hadamard gates again
  6. repeat the optimal number of times
  7. measure the qubits

### Notes on My Version

This script also contains placeholder or simplified versions of higher-order Toffoli-style logic:

* `TOFF3_gate`
* `TOFFn_gate`

These appear to have been simplified during development rather than left as full recursive constructions. So the script reflects both tutorial ideas and my own working/testing stage, rather than a polished general-purpose simulator.

### Outcome

The final call:

```python
workspace = np.array([[1.]])
groverSearch(6)
```

runs a 6-qubit Grover-style search using the NumPy-based simulator.

---

## Part 3 – PyTorch / CPU-GPU Version

The third script follows the ENCCS Part 3 tutorial by replacing NumPy-based workspace operations with **PyTorch** tensor operations. The tutorial explicitly recommends moving the workspace to PyTorch memory and using PyTorch in place of many NumPy calls. ([ENCCS][3])

### Main Changes

Compared with the NumPy version:

* `workspace` becomes a PyTorch tensor
* `pushQubit`, `applyGate`, `tosQubit`, and `probQubit` are rewritten using PyTorch operations
* the code checks whether CUDA is available:

  * prints `"GPU available"` if a GPU is present
  * otherwise falls back to CPU

This matches the tutorial’s explanation that PyTorch can run both on CPU and GPU, and that the workspace should live entirely in PyTorch-managed memory. ([ENCCS][3])

### What My Script Does

In the final version I ran:

* GPU availability is checked
* the simulator falls back to CPU if no GPU is present
* `groverSearch(16, printProb=False)` is timed using PyTorch tensors on CPU

So although the tutorial’s Part 3 is about GPU acceleration, in my environment the script reported that only CPU execution was available.

---

## How to Run

### Part 1 / Part 2 (NumPy)

```bash
python3 script_name.py
```

### Part 3 (PyTorch)

```bash
python3 script_name.py
```

If PyTorch with CUDA support is available, the Part 3 version can use a GPU. Otherwise it runs on CPU. ([ENCCS][3])

---

## Summary of Progression

This tutorial sequence showed a clear development path:

1. **Build a basic simulator**

   * represent qubits and quantum states using vectors and matrices
   * manage qubit ordering using a stack-machine approach

2. **Apply the simulator to an algorithm**

   * extend the simulator with oracle logic
   * implement Grover-style amplitude amplification

3. **Improve execution model**

   * replace NumPy operations with PyTorch
   * move the workspace to CPU/GPU tensor memory

This mirrors the structure of the ENCCS tutorial series closely. ([ENCCS][1])

---

## Conclusions

Working through these three scripts gave a practical introduction to how a quantum computer simulator can be built from scratch.

The main takeaways were:

* a small set of vector and matrix operations is enough to build a working educational simulator
* gate application depends heavily on keeping qubit ordering under control
* measurement requires both probability calculation and state collapse
* Grover’s search can be implemented on top of the same basic simulator structure
* PyTorch provides a natural route to CPU/GPU-backed simulation, even if GPU hardware is not available locally

Overall, this folder documents a progression from a basic educational simulator to an algorithmic extension and then to a hardware-aware implementation using PyTorch.

[1]: https://enccs.se/tutorials/2024/02/quantum-computing-for-beginners-part-1/?utm_source=chatgpt.com "Program your own quantum computer - Part 1"
[2]: https://enccs.se/tutorials/2024/02/quantum-computing-for-beginners-part-2-grovers-search/?utm_source=chatgpt.com "Program your own quantum computer- Part 2 (Grover's ..."
[3]: https://enccs.se/tutorials/2024/02/quantum-computing-for-beginners-part-3-gpus/?utm_source=chatgpt.com "Program your own quantum computer - Part 3 - GPUs"
