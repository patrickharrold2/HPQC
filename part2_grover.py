import numpy as np

def pushQubit(name,weights):
    global workspace
    global namestack
    if workspace.shape == (1,1):                  # if workspace empty
        namestack = []                            # then reset
    namestack.append(name)                        # push name
    weights = weights/np.linalg.norm(weights)     # normalize
    weights = np.array(weights,dtype=workspace[0,0].dtype)
    workspace = np.reshape(workspace,(1,-1))      # to row vector
    workspace = np.kron(workspace,weights)

# def applyGate(gate,*names):
#     global workspace
#     for name in names:                   # move qubits to TOS
#         tosQubit(name)
#     workspace = np.reshape(workspace,(-1,gate.shape[0]))
#     np.matmul(workspace,gate.T,out=workspace)

def applyGate(gate,*names):
    global workspace
    if list(names) != namestack[-len(names):]: # reorder stack
        for name in names: # if necessary
            tosQubit(name)
    workspace = np.reshape(workspace,(-1,2**(len(names))))
    subworkspace = workspace[:,-gate.shape[0]:]
    np.matmul(subworkspace,gate.T,out=subworkspace)

#INSSTRUCTION 3
def tosQubit(name):
    global workspace
    global namestack
    k = len(namestack)-namestack.index(name)    # qubit pos
    if k > 1:                                   # if non-trivial
        namestack.append(namestack.pop(-k))         # rotate name stack
    workspace = np.reshape(workspace,(-1,2,2**(k-1)))
    workspace = np.swapaxes(workspace,-2,-1)

#INSTRUCTION 4
def probQubit(name):
    global workspace
    tosQubit(name)
    workspace = np.reshape(workspace,(-1,2))
    prob = np.linalg.norm(workspace,axis=0)**2
    return prob/prob.sum()                 # make sure sum is one

def measureQubit(name):
    global workspace
    global namestack
    prob = probQubit(name)
    measurement = np.random.choice(2,p=prob)
    workspace = (workspace[:,[measurement]]/
                 np.sqrt(prob[measurement]))
    namestack.pop()
    return str(measurement)

def toffEquiv_gate(q1,q2,q3):               # define Toffoli gate
    applyGate(H_gate,q3)                    # using H, T, T*, CNOT
    applyGate(CNOT_gate,q2,q3)
    applyGate(Tinv_gate,q3)
    applyGate(CNOT_gate,q1,q3)
    applyGate(T_gate,q3)
    applyGate(CNOT_gate,q2,q3)
    applyGate(Tinv_gate,q3)
    applyGate(CNOT_gate,q1,q3)
    applyGate(T_gate,q2)
    applyGate(T_gate,q3)
    applyGate(H_gate,q3)
    applyGate(CNOT_gate,q1,q2)
    applyGate(T_gate,q1)
    applyGate(Tinv_gate,q2)
    applyGate(CNOT_gate,q1,q2)

#PART 2: GROVERS SEARCH
def zero_booleanOracle(qubits,result): # all qubits zero?
    # if all qubits==0 return 1 else return 0
    for qubit in qubits:             # negate all inputs
        applyGate(X_gate,qubit)
    TOFFn_gate(qubits,result)        # compute AND
    for qubit in qubits:             # restore inputs
        applyGate(X_gate,qubit)

def zero_phaseOracle(qubits):            # all qubits zero?
    # if all qubits==0 return -weight else return weight
    for qubit in qubits:                 # negate all inputs
        applyGate(X_gate,qubit)
    applyGate(Z_gate,*namestack)         # controlled Z gate
    for qubit in qubits:                 # restore inputs
        applyGate(X_gate,qubit)

def sample_phaseOracle(qubits):          # sample function
        # if all f(x)==1 return -weight else return weight
    applyGate(X_gate,qubits[1])          # negate qubit 1
    applyGate(Z_gate,*namestack)         # controlled Z gate
    applyGate(X_gate,qubits[1])          # restore qubit 1

def groverSearch(n, printProb=True):
    optimalTurns = int(np.pi/4*np.sqrt(2**n)-1/2)   # iterations
    qubits = list(range(n))                         # generate qubit names
    for qubit in qubits:                            # initialize qubits
        pushQubit(qubit,[1,1])
    for k in range(optimalTurns):                   # Grover iterations:
        sample_phaseOracle(qubits)                  # apply phase oracle
        for qubit in qubits:                        # H-gate all qubits
            applyGate(H_gate,qubit)
        zero_phaseOracle(qubits)                    # apply 0 phase oracle
        for qubit in qubits:                        # H-gate all qubits
            applyGate(H_gate,qubit)
        if printProb:                               # peek probabilities
            print(probQubit(qubits[0]))             # to show convergence
    for qubit in reversed(qubits):                  # print result
        print(measureQubit(qubit),end="")


#GATES
X_gate = np.array([[0, 1],                      # Pauli X gate
                   [1, 0]])                     # = NOT gate

Y_gate = np.array([[ 0,-1j],                    # Pauli Y gate
                   [1j,  0]])                   # = SHZHZS

Z_gate = np.array([[1, 0],                      # Pauli Z gate
                   [0,-1]])                     # = P(pi) = S^2
                                                # = HXH

H_gate = np.array([[1, 1],                      # Hadamard gate
                   [1,-1]]) * np.sqrt(1/2)

S_gate = np.array([[1, 0],                      # Phase gate
                   [0,1j]])                     # = P(pi/2) = T^2

T_gate = np.array([[1,                0],       # = P(pi/4)
                   [0,np.exp(np.pi/-4j)]])

Tinv_gate = np.array([[1, 0],                   # = P(-pi/4)
                      [0,np.exp(np.pi/4j)]])    # = T^-1

def P_gate(phi):                                # Phase shift gate
    return np.array([[1,             0],
                     [0,np.exp(phi*1j)]])

def Rx_gate(theta):                             # Y rotation gate
    return np.array([[np.cos(theta/2),-1j*np.sin(theta/2)],
                     [-1j*np.sin(theta/2),np.cos(theta/2)]])

def Ry_gate(theta):                             # Y rotation gate return
    return np.array([[np.cos(theta/2),-np.sin(theta/2)],
              [np.sin(theta/2), np.cos(theta/2)]])

def Rz_gate(theta):                             # Z rotation gate
    return np.array([[np.exp(-1j*theta/2),                0], [                  0, np.exp(1j*theta/2)]])

# def TOFF3_gate(q1,q2,q3,q4): # q4 = q4 XOR (q1 AND q2 AND q3)
#     pushQubit("temp",[1,0]) # push a zero temporary qubit
#     applyGate(TOFF_gate,q1,q2,"temp") # t = q1 AND q2
#     applyGate(TOFF_gate,"temp",q3,q4) # q4 = q4
#     measureQubit("temp") # pop temp qubit - PROBLEM HERE!

def TOFF3_gate(q1,q2,q3,q4):
    applyGate(X_gate,q1,q2,q3,q4)

# def TOFFn_gate(ctl,result): # result = result XOR AND(qubits)
#     n = len(ctl)
#     if n == 0:
#         applyGate(X_gate,result)
#     if n == 1:
#         applyGate(CNOT_gate,ctl[0],result)
#     elif n == 2:
#         applyGate(TOFF_gate,ctl[0],ctl[1],result)
#     elif n > 2:
#         k=0
#         while "temp"+str(k) in namestack:
#             k=k+1
#         temp = "temp"+str(k)        # generate unique name
#         pushQubit(temp,[1,0])       # push zero temp qubit
#         applyGate(TOFF_gate,ctl[0],ctl[1],temp) # apply TOFF
#         ctl.append(temp)            # add temp to controls
#         TOFFn_gate(ctl[2:],result)  # recursion
#         applyGate(TOFF_gate,ctl[0],ctl[1],temp) # uncompute temp
#         measureQubit(temp)          # pop temp

def TOFFn_gate(ctl,result):
    applyGate(X_gate,*ctl,result)

CNOT_gate = np.array([[1, 0, 0, 0],             # Ctled NOT gate
                      [0, 1, 0, 0],             #=XORgate
                      [0, 0, 0, 1],
                      [0, 0, 1, 0]])

CZ_gate = np.array([[1, 0, 0, 0],               # Ctled Z gate
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0,-1]])

SWAP_gate = np.array([[1, 0, 0, 0],             # Swap gate
                      [0, 0, 1, 0],
                      [0, 1, 0, 0],
                      [0, 0, 0, 1]])

TOFF_gate = np.array([[1, 0, 0, 0, 0, 0, 0, 0], # Toffoli gate
                     [0, 1, 0, 0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 1, 0, 0, 0, 0],
                     [0, 0, 0, 0, 1, 0, 0, 0],
                     [0, 0, 0, 0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 1],
                     [0, 0, 0, 0, 0, 0, 1, 0]])


# workspace = np.array([[1.]])
# for i in range(16):
#     pushQubit([1,0])                      # push a zero qubit
#     applyGate(H_gate)                     # set equal 0 and 1 probability
#     pushQubit([1,0])                      # push a 2nd zero qubit
#     applyGate(H_gate)                     # set equal 0 and 1 probability
#     pushQubit([1,0])                      # push a dummy zero qubit
#     applyGate(TOFF_gate)                  # compute Q3 = Q1 AND Q2
#     q3 = measureQubit()                   # pop qubit 3
#     q2 = measureQubit()                   # pop qubit 2
#     q1 = measureQubit()                   # pop qubit 1
#     print(q1+q2+q3,end=",")

# workspace = np.array([[1.]])        # create empty qubit stack
# pushQubit("Q1",[1,1])               # push a qubit
# print(np.reshape(workspace,(1,-1))) # print workspace as vector print(namestack)
# pushQubit("Q2",[0,1])               # push a 2nd qubit
# print(np.reshape(workspace,(1,-1))) # print workspace as vector print(namestack))
# print(namestack)
# tosQubit("Q1")                       # swap qubits
# print(np.reshape(workspace,(1,-1)))
# print(namestack)
# applyGate(H_gate,"Q2")                    # H gate on qubit 2
# print(np.reshape(workspace,(1,-1)))       # turns a 0 qubit to 1
# print(namestack)                          # with 50% probability

# workspace = np.array([[1.]])
# pushQubit("Q1",[1,0])
# applyGate(H_gate,"Q1")
# print("Q1 probabilities:", probQubit("Q1")) # peek Q1 prob
# pushQubit("Q2",[0.6,0.8])
# print("Q2 probabilities:", probQubit("Q2")) # peek Q2 prob
# print(measureQubit("Q1"), measureQubit("Q2"))

# workspace = np.array([[1.+0j]])           # prep COMPLEX array
# for i in range(16):                       # test function
#     pushQubit("Q1",[1,1])
#     pushQubit("Q2",[1,1])
#     pushQubit("Q3",[1,0])
#     toffEquiv_gate("Q1","Q2","Q3")        # compute Q3 = Q1 AND Q2
#     print(measureQubit("Q1")+measureQubit("Q2")+ measureQubit("Q3"), end=",")

# workspace = np.array([[1.]])                  # test!
# for i in range(20):                           # generate truth table
#     pushQubit("Q1",[1,1])
#     pushQubit("Q2",[1,1])
#     pushQubit("Q3",[1,1])
#     pushQubit("Q4",[1,0])                         # Q4 starts at zero so
#     TOFF3_gate("Q1","Q2","Q3","Q4")               # Q4 = AND of Q1 thru Q3
#     print("".join([measureQubit(q) for q in ["Q1","Q2","Q3","Q4"]]), end=",")

# workspace = np.array([[1]],dtype=np.single)     # test!
# for i in range(20):                 # generate truth table
#     pushQubit("Q1",[1,1])
#     pushQubit("Q2",[1,1])
#     pushQubit("Q3",[1,1])
#     pushQubit("Q4",[1,0])               # Q4 starts at zero, becomes
#     TOFFn_gate(["Q1","Q2","Q3"],"Q4")   # AND of Q1 thru Q3
#     print("".join([measureQubit(q) for q in
#                ["Q1","Q2","Q3","Q4"]]),end=",")

# workspace = np.array([[1]],dtype=np.single)
# for i in range(20):
#     pushQubit("Q1",[1,1])
#     pushQubit("Q2",[1,1])
#     pushQubit("Q3",[1,1])
#     pushQubit("Q4",[1,0])
#
#     TOFF3_gate("Q1","Q2","Q3","Q4")
#     print("".join([measureQubit(q) for q in ["Q1","Q2","Q3","Q4"]]),end="/")
#     pushQubit("Q1",[1,1])
#     pushQubit("Q2",[1,1])
#     pushQubit("Q3",[1,1])
#     pushQubit("Q4",[1,0])
#     TOFFn_gate(["Q1","Q2","Q3"],"Q4")
#     print("".join([measureQubit(q) for q in ["Q1","Q2","Q3","Q4"]]),end=",")

workspace = np.array([[1.]])              # initialize workspace
groverSearch(6)                           # (only reals used here)
