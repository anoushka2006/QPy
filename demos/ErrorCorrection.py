import numpy as np

from numpy import random


import matplotlib.image as image

import matplotlib.pyplot as plt


from qpy import *


def prep_state_angle(theta):

    state = zero

    state = Rx(theta)@state
    return state


#Shors encoding/decoding circuit

def shor_encode(state):

    num_qubits = int(np.log2(len(state)))
    

    state = cnot_nonadj(0, 3, num_qubits)@state

    state = cnot_nonadj(0, 6, num_qubits)@state


    state = add_gate(H, 0, num_qubits)@state

    state = add_gate(H, 3, num_qubits)@state

    state = add_gate(H, 6, num_qubits)@state
    

    state = cnot_adj(0, 1, num_qubits)@state

    state = cnot_adj(3, 4, num_qubits)@state

    state = cnot_adj(6, 7, num_qubits)@state
    

    state = cnot_nonadj(0, 2, num_qubits)@state

    state = cnot_nonadj(3, 5, num_qubits)@state

    state = cnot_nonadj(6, 8, num_qubits)@state

    return state 



def shor_decode(state):

    num_qubits = int(np.log2(len(state)))
    

    state = cnot_adj(0, 1, num_qubits)@state

    state = cnot_adj(3, 4, num_qubits)@state

    state = cnot_adj(6, 7, num_qubits)@state
    

    state = cnot_nonadj(0, 2, num_qubits)@state

    state = cnot_nonadj(3, 5, num_qubits)@state

    state = cnot_nonadj(6, 8, num_qubits)@state
    

    state = TOFFOLI(1, 2, 0, num_qubits)@state

    state = TOFFOLI(4, 5, 3, num_qubits)@state

    state = TOFFOLI(7, 8, 6, num_qubits)@state
    

    state = add_gate(H, 0, num_qubits)@state

    state = add_gate(H, 3, num_qubits)@state

    state = add_gate(H, 6, num_qubits)@state
    

    state = cnot_nonadj(0, 3, num_qubits)@state

    state = cnot_nonadj(0, 6, num_qubits)@state

    state = TOFFOLI(3, 6, 0, num_qubits)@state
    
    return state    



# With no errors

ratio_list = []

theta_list = np.linspace(0, 2*np.pi, 20)


for theta in theta_list:
    

    #print (theta)


    count1 = 0

    count0 = 0
    

    st = prep_state_angle(theta)

    qubits = [st] + [zero]*8
    state = kron(qubits)
        

    stt = shor_encode(state)

    stt2 = shor_decode(stt)
    

    for i in range(100):
           

        stt_copy, output = measure(np.copy(stt2), 0)

        # st_m = measure(st)
        

        if output == 1:

            count1 = count1 + 1

        if output == 0:

            count0 = count0 + 1
            

    ratio = count1/(count0 + count1)

    ratio_list.append(ratio)
        

plt.plot(theta_list, ratio_list, label = 'Observed Ratio')

plt.plot(theta_list, (1 - np.cos(theta_list))/2, label = 'Expected Ratio')

plt.title("Error Correction Demo: No Errors")

plt.xlabel("Rotation Angle $\\theta$")

plt.ylabel("Fractional |1⟩ population")

plt.legend()

plt.show()




#applying 1 error

ratio_list = []

theta_list = np.linspace(0, 2*np.pi, 20) 


for theta in theta_list:

    count1 = 0

    count0 = 0
    

    st = prep_state_angle(theta)

    qubits = [st] + [zero]*8
    state = kron(qubits)
        

    enc = shor_encode(state)
    

    g = random.randint(3)

    target = random.randint(9)

    if g == 0:

        enc = add_gate(X, target, 9)@enc

    elif g == 1:

        enc = add_gate(Y, target, 9)@enc

    else:

        enc = add_gate(Z, target, 9)@enc
        

    stt2 = shor_decode(enc)
    
    

    for i in range(100):
           

        stt_copy, output = measure(np.copy(stt2), 0)
        

        if output == 1:

            count1 = count1 + 1

        if output == 0:

            count0 = count0 + 1
            

    ratio = count1/(count0 + count1)

    ratio_list.append(ratio)
        

plt.plot(theta_list, ratio_list, label = 'Observed Ratio')

plt.plot(theta_list, (1 - np.cos(theta_list))/2, label = 'Expected Ratio')

plt.title("Error in 1 qubit value")

plt.xlabel("Rotation Angle $\\theta$")

plt.ylabel("Fractional |1⟩ population")

plt.legend()

plt.show()




#demo for if there is an error with two qubits

#algorithm only works if one qubit is switched


#Applying 2 errors

ratio_list = []

theta_list = np.linspace(0, 2*np.pi, 20)


for theta in theta_list:

    count1 = 0

    count0 = 0
    

    st = prep_state_angle(theta)

    qubits = [st] + [zero]*8
    state = kron(qubits)
        

    enc = shor_encode(state)
    

    g = random.randint(3)

    target = random.randint(9)

    if g == 0:

        enc = add_gate(X, target, 9)@enc

    elif g == 1:

        enc = add_gate(Y, target, 9)@enc

    else:

        enc = add_gate(Z, target, 9)@enc
        

    g = random.randint(3)

    target = random.randint(9)

    if g == 0:

        enc = add_gate(X, target, 9)@enc

    elif g == 1:

        enc = add_gate(Y, target, 9)@enc

    else:

        enc = add_gate(Z, target, 9)@enc
        

    stt2 = shor_decode(enc)
    
    
    

    for i in range(100):
           

        stt_copy, output = measure(np.copy(stt2), 0)

        # st_m = measure(st)
        

        if output == 1:

            count1 = count1 + 1

        if output == 0:

            count0 = count0 + 1
            

    ratio = count1/(count0 + count1)

    ratio_list.append(ratio)
        

plt.plot(theta_list, ratio_list, label = 'Observed Ratio')

plt.plot(theta_list, (1 - np.cos(theta_list))/2, label = 'Expected Ratio')

plt.title("Error in 2 qubit values")

plt.xlabel("Rotation Angle $\\theta$")

plt.ylabel("Fractional |1⟩ population")

plt.legend()

plt.show()