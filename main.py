import numpy as np

from qpy.linalg import *
from qpy.gates import *
from qpy.measurement import *


# function to generate a GHZ State
def generate_ghz_state(num_qubits):
    # Initialising the state to |0...0⟩
    ghz_state = apply_kron([zero] * (num_qubits))

    # Apply Hadamard gate to the last qubit
    ghz_state = apply_gate(H,0,num_qubits)@ghz_state

    # Apply CNOT gates to create GHZ state
    for i in range(num_qubits - 1):
        ghz_state = cnot_adj(i, i+1, num_qubits)@ghz_state
            
    return ghz_state



# implement CNOT on adjacent qubits
def cnot_adj(controlq, targetq, num_qubits):
    if targetq != controlq + 1:
        raise ValueError("Control and Target qubits must be adjacent.")
    
    #pad CNOT matrix 
    start_padding = controlq
    end_padding = num_qubits - (targetq + 1)
    operator = apply_kron([*[I]*start_padding, cnot, *[I]*end_padding])

    return operator



#implementing CNOT on non-adjacent qubits 
def cnot_nonadj(control_qubit:int, target_qubit:int, num_qubits:int) -> np.ndarray:
    
    if control_qubit == target_qubit:
        raise ValueError("Control and Target qubits must be different.")
    
    if not (0<= control_qubit <= num_qubits) or not (0<= target_qubit <= num_qubits):
        raise ValueError("Error")
        

    # Apply the controlled NOT gate with padding
    if control_qubit < target_qubit:
        operator = apply_kron([*[I]*(control_qubit), np.outer(zero,zero), *[I]*(num_qubits - control_qubit - 1)]) + apply_kron([*[I]*(control_qubit), np.outer(one,one), *[I]*(target_qubit - control_qubit - 1), X, *[I]*(num_qubits - target_qubit - 1)])
    else: 
        operator = apply_kron([*[I]*(control_qubit), np.outer(zero,zero), *[I]*(num_qubits - control_qubit - 1)]) + apply_kron([*[I]*(target_qubit), X, *[I]*(control_qubit - target_qubit - 1), np.outer(one,one), *[I]*(num_qubits - control_qubit - 1)])
        
    return operator



# controlled unitary gate
def control_gate(gate, control_qubit, target_qubit, num_qubits):
    
    if control_qubit == target_qubit:
        raise ValueError("Control and Target qubits must be different.")
    
    if not (0<= control_qubit <= num_qubits) or not (0<= target_qubit <= num_qubits):
        raise ValueError("Error")
        

    # Apply the controlled gate with padding
    if control_qubit < target_qubit:
        operator = apply_kron([*[I]*(control_qubit), np.outer(zero,zero), *[I]*(num_qubits - control_qubit - 1)]) + apply_kron([*[I]*(control_qubit), np.outer(one,one), *[I]*(target_qubit - control_qubit - 1), gate, *[I]*(num_qubits - target_qubit - 1)])
    else: 
        operator = apply_kron([*[I]*(control_qubit), np.outer(zero,zero), *[I]*(num_qubits - control_qubit - 1)]) + apply_kron([*[I]*(target_qubit), gate, *[I]*(control_qubit - target_qubit - 1), np.outer(one,one), *[I]*(num_qubits - control_qubit - 1)])
        
    return operator

