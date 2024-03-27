# import numpy as np

# from qpy.gates import *

# #function to apply kronecker function to multiple operators at once
# def apply_kron(operators):
#     result = operators[0]
#     for op in operators[1:]:
#         result = np.kron(result, op)
#     return result

# def dot_prod(operators):
#     result = operators[0]
#     for op in operators[1:]:
#         result = np.dot(result, op)
#     return result


# # function to apply any gate to a target qubit
# def apply_gate(gate:np.ndarray, targetq:int, num_qubit:int) -> np.ndarray:
#     start_pad = targetq
#     end_pad = num_qubit - (targetq + 1)
    
#     operator = apply_kron([*[I]*start_pad, gate, *[I]*end_pad])
    
#     return operator
