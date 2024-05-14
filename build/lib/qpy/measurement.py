import numpy as np


from qpy.gates import *


def dag(state):

    return state.T.conj()


def measure(state, qubit_index):

    # Measuring the first qubit

    num_qubits = int(np.log2(len(state)))
    M0 = kron([*[I]*(qubit_index), np.outer(zero,zero), *[I]*(num_qubits - qubit_index -1)])
    M1 = kron([*[I]*(qubit_index), np.outer(one, one), *[I]*(num_qubits - qubit_index -1)])


    # Dagger

    P0 = dag(state) @ dag(M0) @ M0 @ state

    P1 = dag(state) @ dag(M1) @ M1 @ state


    assert np.isclose(P0 + P1, 1)


    outcome = 0 if np.random.rand() < P0 else 1

    if outcome == 0:

        #collapse state to 0

        state = M0 @ state / np.sqrt(P0)

    else:

        #collapse state to 1

        state = M1 @ state / np.sqrt(P1)
        

    return state, outcome