import numpy as np
import matplotlib.pyplot as plt

from qpy.gates import *
from qpy.measurement import *

#generating a bell pair
def bell_pair():
    bell_state = np.kron(zero,zero)
    bell_state = np.dot(np.kron(H, I), bell_state)
    bell_state = np.dot(cnot, bell_state)
    
    return bell_state


def teleport_quantum_state(original_state):
    """Teleports a quantum state using an entangled Bell state."""
    bell_state = bell_pair()

    state = np.kron(original_state, bell_state)
    
    # Apply CNOT by original state
    state = cnot_nonadj(0, 1, 3)@state

    # Apply Hadamard to controlled qubit
    state = add_gate(H, 0, 3)@state

    # Measure both control qubits
    state, outcome0 = measure(state, 0)
    
    state, outcome1 = measure(state, 1)


    if outcome1 == 1:
        state = add_gate(X, 2, 3)@state
    if outcome0 == 1:
        state = add_gate(Z, 2, 3)@state

    return state



# Preparing state angles and rotating it along the X axis
def prep_state_angle(theta):
    state = zero
    state = Rx(theta)@state
    return state

ratio_list = []
theta_list = np.linspace(0, 2*np.pi, 20)

for theta in theta_list:
    
    count1 = 0
    count0 = 0
    
    for i in range(500):
      
        st = prep_state_angle(theta)
        
        stt = teleport_quantum_state(st)
        stt, output= measure(stt, 2)
        
        if output == 1:
            count1 = count1 + 1
        if output == 0:
            count0 = count0 + 1
            
    ratio = count1/(count0 + count1)
    ratio_list.append(ratio)
        

# Plotting observed and expected results 
plt.plot(theta_list, ratio_list, label = 'Observed Ratio')
plt.plot(theta_list, (1 - np.cos(theta_list))/2, label = 'Expected Ratio')
plt.title("Teleportation Demo")
plt.legend()
plt.show()