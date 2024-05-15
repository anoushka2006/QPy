from typing import Iterable

import numpy as np



# Utility: Perform calculations successively on operator matrices
def kron(operators: Iterable[np.ndarray]) -> np.ndarray:
    '''
    Successive kronecker function for multiple operators
    kron([A, B, C]) => np.kron(np.kron(A, B), C)
    '''
    result = operators[0]
    for op in operators[1:]:
        result = np.kron(result, op)
    return result

def dot(operators: Iterable[np.ndarray]) -> np.ndarray:
    '''
    Successive dot product for multiple operators
    dot([A, B, C]) => np.dot(np.dot(A, B), C)
    '''
    result = operators[0]
    for op in operators[1:]:
        result = np.dot(result, op)
    return result
 


# Utility: Add gate logic
def add_gate(gate:np.ndarray, target_qubit:int, num_qubits:int) -> np.ndarray:
    '''Add a gate at a given qubit'''
    start_pad = target_qubit
    end_pad = num_qubits - (target_qubit + 1)
    
    operator = kron([I]*start_pad + [gate] + [I]*end_pad)
    
    return operator

def control_gate(gate: np.ndarray, control_qubit: int, target_qubit: int, num_qubits: int) -> np.ndarray:
    '''Add a control gate at a given qubit'''
    if control_qubit == target_qubit:
        raise ValueError("Control and Target qubits must be different.")
    
    if not (0 <= control_qubit < num_qubits):
        raise ValueError("Control Qubit not within given number of qubits")

    if not (0 <= target_qubit < num_qubits):
        raise ValueError("Target Qubit not within given number of qubits")

    # Apply the controlled gate with padding
    if control_qubit < target_qubit:
        operator = \
            add_gate(np.outer(zero,zero), control_qubit, num_qubits) + \
            kron([I]*control_qubit + [np.outer(one,one)] + [I]*(target_qubit - control_qubit - 1) + [gate] + [I]*(num_qubits - target_qubit - 1))
    else: 
        operator = \
            add_gate(np.outer(zero,zero), control_qubit, num_qubits) + \
            kron([I]*(target_qubit) + [gate] + [I]*(control_qubit - target_qubit - 1) + [np.outer(one,one)] + [I]*(num_qubits - control_qubit - 1))
        
    return operator



# Variables: Zero, one, and half states
zero = np.array([1,0])
one = np.array([0,1])
plus = 1/np.sqrt(2) * np.array([1,1])



# Variables: Gate matrices
I = np.eye(2)
'''Identity'''

Px = np.array([[0,1], 
               [1,0]])
'''Pauli-X'''

Py = np.array([[0,-1j],
               [1j,0]])
'''Pauli-Y'''

Pz = np.array([[1,0],
               [0,-1]])
'''Pauli-Z'''

H = 1/np.sqrt(2)*np.array([[1,1],
                           [1,-1]])
'''Hadamard Gate'''

S = np.array([[1,0],
              [0,1j]])
'''Phase (S,Q)'''

T = np.array([[1,0],
              [0,np.exp(1j*np.pi/4)]])
'''pi/8'''

CX = np.array([[1,0,0,0],
                 [0,1,0,0],
                 [0,0,0,1],
                 [0,0,1,0]])
'''Controlled X'''

CZ = np.array([[1,0,0,0],
               [0,1,0,0],
               [0,0,1,0],
               [0,0,0,-1]])
'''Controlled Z'''

swap = np.array([[1,0,0,0],
                 [0,0,1,0],
                 [0,1,0,0],
                 [0,0,0,1]])
'''Swap'''

def Rx(theta):
    '''Rotation in X by radian angle theta'''
    return np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                     [-1j*np.sin(theta/2), np.cos(theta/2)]])

def Rz(theta):
    '''Rotation in Z by radian angle theta'''
    return np.array([[1,0],[0, np.exp(1j*theta)]])



def CX_ADJ(control_qubit:int, target_qubit:int, num_qubits:int) -> np.ndarray:
    '''CX on adjacent qubits'''
    if target_qubit != control_qubit + 1:
        raise ValueError("Control and Target qubits must be adjacent.")
    
    start_padding = control_qubit
    end_padding = num_qubits - (target_qubit + 1)
    operator = kron([I]*start_padding + [CX] + [I]*end_padding)

    return operator



def CX_NONADJ(control_qubit:int, target_qubit:int, num_qubits:int) -> np.ndarray:
    '''CX on non-adjacent qubits'''
    if control_qubit == target_qubit:
        raise ValueError("Control and Target qubits must be different.")
    
    if not (0 <= control_qubit < num_qubits):
        raise ValueError("Control Qubit not within given number of qubits")
    
    if not (0 <= target_qubit < num_qubits):
        raise ValueError("Target Qubit not within given number of qubits")
    
    if control_qubit < target_qubit:
        operator = \
            add_gate(np.outer(zero,zero), control_qubit, num_qubits) + \
            kron([I]*(control_qubit) + [np.outer(one,one)] + [I]*(target_qubit - control_qubit - 1) + [Px] + [I]*(num_qubits - target_qubit - 1))
    else: 
        operator = \
            add_gate(np.outer(zero,zero), control_qubit, num_qubits) + \
            kron([I]*(target_qubit) + [Px] + [I]*(control_qubit - target_qubit - 1) + [np.outer(one,one)] + [I]*(num_qubits - control_qubit - 1))
        
    return operator



def generate_ghz_state(num_qubits:int) -> np.ndarray:
    '''Function to generate a Greenberger-Horne-Zeilinger state'''
    # Initialising the state to |0...0⟩
    ghz_state = kron([zero] * (num_qubits))

    # Apply Hadamard gate to the last qubit
    ghz_state = add_gate(H,0,num_qubits)@ghz_state

    # Apply CNOT gates to create GHZ state
    for i in range(num_qubits - 1):
        ghz_state = CX_ADJ(i, i+1, num_qubits)@ghz_state
            
    return ghz_state



def TOFFOLI(control_qubit_1:int, control_qubit_2:int, target_qubit:int, num_qubits:int) -> np.ndarray:
    '''TOFFOLI Gate'''
    if control_qubit_1 == target_qubit or control_qubit_2 == target_qubit:
        raise ValueError("Control and Target qubits must be different.")
    
    if not (0 <= control_qubit_1 < num_qubits):
        raise ValueError("First Control Qubit not within given number of qubits")

    if not (0 <= control_qubit_2 < num_qubits):
        raise ValueError("Second Control Qubit not within given number of qubits")
    
    if not (0 <= target_qubit < num_qubits):
        raise ValueError("Target Qubit not within given number of qubits")
        
    # Ensure control_qubits are ordered in ascending order of indices
    c1, c2 = sorted([control_qubit_1, control_qubit_2])

    # Apply the controlled NOT gate with padding
    if c2 < target_qubit:
        term1 = kron([I]*(c1) + [np.outer(zero,zero)] + [I]*(c2 - c1 - 1) + [np.outer(zero,zero)] + [I]*(target_qubit - c2 - 1) + [I] + [I]*(num_qubits - target_qubit - 1))
        term2 = kron([I]*(c1) + [np.outer(one,one)] + [I]*(c2 - c1 - 1) + [np.outer(zero,zero)] + [I]*(target_qubit - c2 - 1) + [I] + [I]*(num_qubits - target_qubit - 1))
        term3 = kron([I]*(c1) + [np.outer(zero,zero)] + [I]*(c2 - c1 - 1) + [np.outer(one,one)] + [I]*(target_qubit - c2 - 1) + [I] + [I]*(num_qubits - target_qubit - 1))
        term4 = kron([I]*(c1) + [np.outer(one,one)] + [I]*(c2 - c1 - 1) + [np.outer(one,one)] + [I]*(target_qubit - c2 - 1) + [Px] + [I]*(num_qubits - target_qubit - 1))
        operator = term1 + term2 + term3 + term4
        
    elif c1 < target_qubit < c2: # If target qubit is in the middle of both controls
        term1 = kron([I]*(c1) + [np.outer(zero,zero)] + [I]*(target_qubit - c1 - 1) + [I] + [I]*(c2 - target_qubit - 1) + [np.outer(zero,zero)] + [I]*(num_qubits - c2 - 1))
        term2 = kron([I]*(c1) + [np.outer(one,one)] + [I]*(target_qubit - c1 - 1) + [I] + [I]*(c2 - target_qubit - 1) + [np.outer(zero,zero)] + [I]*(num_qubits - c2 - 1))
        term3 = kron([I]*(c1) + [np.outer(zero,zero)] + [I]*(target_qubit - c1 - 1) + [I] + [I]*(c2 - target_qubit - 1) + [np.outer(one,one)] + [I]*(num_qubits - c2 - 1))
        term4 = kron([I]*(c1) + [np.outer(one,one)] + [I]*(target_qubit - c1 - 1) + [Px] + [I]*(c2 - target_qubit - 1) + [np.outer(one,one)] + [I]*(num_qubits - c2 - 1))
        operator = term1 + term2 + term3 + term4
        
    elif target_qubit < c1: # if target is before both controls
        term1 = kron([I]*(target_qubit) + [I] + [I]*(c1 - target_qubit - 1) + [np.outer(zero,zero)] + [I]*(c2 - c1- 1) + [np.outer(zero,zero)] + [I]*(num_qubits - c2 - 1))
        term2 = kron([I]*(target_qubit) + [I] + [I]*(c1 - target_qubit - 1) + [np.outer(one,one)] + [I]*(c2 - c1- 1) + [np.outer(zero,zero)] + [I]*(num_qubits - c2 - 1))
        term3 = kron([I]*(target_qubit) + [I] + [I]*(c1 - target_qubit - 1) + [np.outer(zero,zero)] + [I]*(c2 - c1- 1) + [np.outer(one,one)] + [I]*(num_qubits - c2 - 1))
        term4 = kron([I]*(target_qubit) + [Px] + [I]*(c1 - target_qubit - 1) + [np.outer(one,one)] + [I]*(c2 - c1- 1) + [np.outer(one, one)] + [I]*(num_qubits - c2 - 1))
        operator = term1 + term2 + term3 + term4
        
    return operator