import numpy as np

# from qpy.linalg import *

#function to apply kronecker function to multiple operators at once
def apply_kron(operators):
    result = operators[0]
    for op in operators[1:]:
        result = np.kron(result, op)
    return result

def dot_prod(operators):
    result = operators[0]
    for op in operators[1:]:
        result = np.dot(result, op)
    return result


# function to apply any gate to a target qubit
def apply_gate(gate:np.ndarray, targetq:int, num_qubit:int) -> np.ndarray:
    start_pad = targetq
    end_pad = num_qubit - (targetq + 1)
    
    operator = apply_kron([*[I]*start_pad, gate, *[I]*end_pad])
    
    return operator


zero = np.array([1,0])
one = np.array([0,1])
plus = 1/np.sqrt(2) * np.array([1,1])
I = np.eye(2)

#Single Qubit Operations
#Pauli-X
X = np.array([[0,1], 
              [1,0]])

#Paui-Y
Y = np.array([[0,-1j],
              [1j,0]])

#Pauli-Z 
Z = np.array([[1,0],
              [0,-1]])

#Hadamard
H = 1/np.sqrt(2)*np.array([[1,1],
                           [1,-1]])

#Phase (S,P)
S = np.array([[1,0],
              [0,1j]])

#pi/8
T = np.array([[1,0],
              [0,np.exp(1j*np.pi/4)]])

#Controlled Not / CX
cnot = np.array([[1,0,0,0],
                 [0,1,0,0],
                 [0,0,0,1],
                 [0,0,1,0]])

#Controlled Z
CZ = np.array([[1,0,0,0],
               [0,1,0,0],
               [0,0,1,0],
               [0,0,0,-1]])

swap = np.array([[1,0,0,0],
                 [0,0,1,0],
                 [0,1,0,0],
                 [0,0,0,1]])

toffoli = np.array([[1,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0],
                    [0,0,0,1,0,0,0,0],
                    [0,0,0,0,1,0,0,0],
                    [0,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,0,1],
                    [0,0,0,0,0,0,1,0]])

#TOFFOLI = 


def Rz(theta):
    return np.array([[1,0],[0, np.exp(1j*theta)]])


# # implement CNOT on adjacent qubits
# def cnot_adj(controlq, targetq, num_qubits):
#     if targetq != controlq + 1:
#         raise ValueError("Control and Target qubits must be adjacent.")
    
#     #pad CNOT matrix 
#     start_padding = controlq
#     end_padding = num_qubits - (targetq + 1)
#     operator = apply_kron([*[I]*start_padding, cnot, *[I]*end_padding])

#     return operator


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
