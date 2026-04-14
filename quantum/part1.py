import numpy as np


def pushQubit(name, weights):
    global workspace
    global namestack
    if workspace.shape == (1, 1):                 # if workspace empty
        namestack = []                            # then reset
    namestack.append(name)                        # push name
    weights = weights / np.linalg.norm(weights)   # normalize
    weights = np.array(weights, dtype=workspace[0, 0].dtype)
    workspace = np.reshape(workspace, (1, -1))    # to row vector
    workspace = np.kron(workspace, weights)


def tosQubit(name):
    global workspace
    global namestack
    k = len(namestack) - namestack.index(name)    # qubit position
    if k > 1:                                     # if non-trivial
        namestack.append(namestack.pop(-k))       # rotate name stack
    workspace = np.reshape(workspace, (-1, 2, 2**(k - 1)))
    workspace = np.swapaxes(workspace, -2, -1)


def applyGate(gate, *names):
    global workspace
    for name in names:                            # move qubits to TOS
        tosQubit(name)
    workspace = np.reshape(workspace, (-1, gate.shape[0]))
    np.matmul(workspace, gate.T, out=workspace)


def probQubit(name):
    global workspace
    tosQubit(name)
    workspace = np.reshape(workspace, (-1, 2))
    prob = np.linalg.norm(workspace, axis=0) ** 2
    return prob / prob.sum()                      # make sure sum is one


def measureQubit(name):
    global workspace
    global namestack
    prob = probQubit(name)
    measurement = np.random.choice(2, p=prob)
    workspace = workspace[:, [measurement]] / np.sqrt(prob[measurement])
    namestack.pop()
    return str(measurement)


def toffEquiv_gate(q1, q2, q3):                   # define Toffoli gate
    applyGate(H_gate, q3)                         # using H, T, T*, CNOT
    applyGate(CNOT_gate, q2, q3)
    applyGate(Tinv_gate, q3)
    applyGate(CNOT_gate, q1, q3)
    applyGate(T_gate, q3)
    applyGate(CNOT_gate, q2, q3)
    applyGate(Tinv_gate, q3)
    applyGate(CNOT_gate, q1, q3)
    applyGate(T_gate, q2)
    applyGate(T_gate, q3)
    applyGate(H_gate, q3)
    applyGate(CNOT_gate, q1, q2)
    applyGate(T_gate, q1)
    applyGate(Tinv_gate, q2)
    applyGate(CNOT_gate, q1, q2)


# GATES
X_gate = np.array([[0, 1],
                   [1, 0]])                       # Pauli X / NOT

Y_gate = np.array([[0, -1j],
                   [1j, 0]])                      # Pauli Y

Z_gate = np.array([[1, 0],
                   [0, -1]])                      # Pauli Z

H_gate = np.array([[1, 1],
                   [1, -1]]) * np.sqrt(1/2)      # Hadamard

S_gate = np.array([[1, 0],
                   [0, 1j]])                      # Phase gate

T_gate = np.array([[1, 0],
                   [0, np.exp(np.pi / -4j)]])

Tinv_gate = np.array([[1, 0],
                      [0, np.exp(np.pi / 4j)]])

CNOT_gate = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1],
                      [0, 0, 1, 0]])

CZ_gate = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, -1]])

SWAP_gate = np.array([[1, 0, 0, 0],
                      [0, 0, 1, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1]])

TOFF_gate = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 1, 0]])


# FINAL PART 1 TEST
workspace = np.array([[1.0 + 0j]])               # prep complex array
for i in range(16):
    pushQubit("Q1", [1, 1])
    pushQubit("Q2", [1, 1])
    pushQubit("Q3", [1, 0])
    toffEquiv_gate("Q1", "Q2", "Q3")            # compute Q3 = Q1 AND Q2
    print(measureQubit("Q1") +
          measureQubit("Q2") +
          measureQubit("Q3"), end=",")1~import numpy as np


def pushQubit(name, weights):
    global workspace
    global namestack
    if workspace.shape == (1, 1):                 # if workspace empty
        namestack = []                            # then reset
    namestack.append(name)                        # push name
    weights = weights / np.linalg.norm(weights)   # normalize
    weights = np.array(weights, dtype=workspace[0, 0].dtype)
    workspace = np.reshape(workspace, (1, -1))    # to row vector
    workspace = np.kron(workspace, weights)


def tosQubit(name):
    global workspace
    global namestack
    k = len(namestack) - namestack.index(name)    # qubit position
    if k > 1:                                     # if non-trivial
        namestack.append(namestack.pop(-k))       # rotate name stack
    workspace = np.reshape(workspace, (-1, 2, 2**(k - 1)))
    workspace = np.swapaxes(workspace, -2, -1)


def applyGate(gate, *names):
    global workspace
    for name in names:                            # move qubits to TOS
        tosQubit(name)
    workspace = np.reshape(workspace, (-1, gate.shape[0]))
    np.matmul(workspace, gate.T, out=workspace)


def probQubit(name):
    global workspace
    tosQubit(name)
    workspace = np.reshape(workspace, (-1, 2))
    prob = np.linalg.norm(workspace, axis=0) ** 2
    return prob / prob.sum()                      # make sure sum is one


def measureQubit(name):
    global workspace
    global namestack
    prob = probQubit(name)
    measurement = np.random.choice(2, p=prob)
    workspace = workspace[:, [measurement]] / np.sqrt(prob[measurement])
    namestack.pop()
    return str(measurement)


def toffEquiv_gate(q1, q2, q3):                   # define Toffoli gate
    applyGate(H_gate, q3)                         # using H, T, T*, CNOT
    applyGate(CNOT_gate, q2, q3)
    applyGate(Tinv_gate, q3)
    applyGate(CNOT_gate, q1, q3)
    applyGate(T_gate, q3)
    applyGate(CNOT_gate, q2, q3)
    applyGate(Tinv_gate, q3)
    applyGate(CNOT_gate, q1, q3)
    applyGate(T_gate, q2)
    applyGate(T_gate, q3)
    applyGate(H_gate, q3)
    applyGate(CNOT_gate, q1, q2)
    applyGate(T_gate, q1)
    applyGate(Tinv_gate, q2)
    applyGate(CNOT_gate, q1, q2)


# GATES
X_gate = np.array([[0, 1],
                   [1, 0]])                       # Pauli X / NOT

Y_gate = np.array([[0, -1j],
                   [1j, 0]])                      # Pauli Y

Z_gate = np.array([[1, 0],
                   [0, -1]])                      # Pauli Z

H_gate = np.array([[1, 1],
                   [1, -1]]) * np.sqrt(1/2)      # Hadamard

S_gate = np.array([[1, 0],
                   [0, 1j]])                      # Phase gate

T_gate = np.array([[1, 0],
                   [0, np.exp(np.pi / -4j)]])

Tinv_gate = np.array([[1, 0],
                      [0, np.exp(np.pi / 4j)]])

CNOT_gate = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1],
                      [0, 0, 1, 0]])

CZ_gate = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, -1]])

SWAP_gate = np.array([[1, 0, 0, 0],
                      [0, 0, 1, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1]])

TOFF_gate = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 1],
                      [0, 0, 0, 0, 0, 0, 1, 0]])


# FINAL PART 1 TEST
workspace = np.array([[1.0 + 0j]])               # prep complex array
for i in range(16):
    pushQubit("Q1", [1, 1])
    pushQubit("Q2", [1, 1])
    pushQubit("Q3", [1, 0])
    toffEquiv_gate("Q1", "Q2", "Q3")            # compute Q3 = Q1 AND Q2
    print(measureQubit("Q1") +
          measureQubit("Q2") +
          measureQubit("Q3"), end=",")
