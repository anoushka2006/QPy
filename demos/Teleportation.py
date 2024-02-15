import numpy as np
import matplotlib.pyplot as plt

from qpy.linalg import *
from qpy.gates import *
from qpy.measurement import *
from main import *

#generating a bell pair
def bell_pair():
    bell_state = np.array([1,0,0,0])
    bell_state = np.dot(np.diag([1,1,1,1]))
    bell_state = np.dot(cnot, bell_state)
    
    return bell_state

def teleport_quantum_state(original_state, num_qubits):
    """Teleports a quantum state using an entangled Bell state."""
    bell_state = bell_pair()

    # Apply CNOT controlled by original state
    teleported_state = cnot_nonadj(np.kron(original_state, bell_state), 0, 2)

    # Apply Hadamard to controlled qubit
    teleported_state = apply_gate(H, 0, num_qubits)

    # Measure both control qubits
    outcome1, teleported_state = measure(teleported_state, 1)
    outcome2, teleported_state = measure(teleported_state, 2)

    # Apply classical communication and corrections
    classical_bits = str(outcome2) + str(outcome1)
    correction_map = {
        "00": np.eye(2),
        "01": X,
        "10": Y,
        "11": Z
    }

    correction = correction_map[classical_bits]
    teleported_state = np.dot(correction, teleported_state)

    return teleported_state




# class Alice(Agent):
#     "Alice sends qubits to Bob using a shared Bell pair"
    
#     def distribute_bell_pair(self, a, b):
#         # creating a bell pair and send one particle to Bob
#         H(a)
#         cnot(a,b)
#         self.qsend(bob, b)
        
#     def teleport(self, q, a):
#         #performing the teleportation
#         cnot(q,a)
#         H(q)
#         #Telling bob whether to apply Pauli-X and -Z over classical channel
#         bob_apply_x = a.measure() # if Bob should apply X
#         bob_apply_z = q.measure() # if Bob should apply Z
#         self.csend(bob, [bob_apply_x, bob_apply_z])
        
#     def run(self):
#         for qsystem in self.qstream:
#             q, a, b = qsystem.qubits # q is state to teleport, a and b are Bell pair
#             self.distribute_bell_pair
#             self.teleport(q, a)
            
            
# class Bob(Agent):
#     "Bob recieves qubits from Alive and measures the results"
    
#     def run(self):
#         measurement_results = []
#         for i in self.qstream: 
#             # Bob receives a qubit from Alice
#             b = self.qrecv(alice)
#             # Bob receives classical instructions from Alice
#             apply_x, apply_z = self.crecv(alice)
#             if apply_x: X(b)
#             if apply_z: Z(b)
            
#             # measuring the output state
#             measurement_results.append(b.measure())
#         # Putting results in output object 
#         self.output(measurement_results)
        
# # preparing the initial states 
# qstream = Qstream(3,10) #3 qubits per trial for 10 trials
# states_to_teleport = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
# for state, qsystem in zip(states_to_teleport, qstream):
#     q = qsystem.qubit(0)
#     if state == 1: 
#         X(q) # flipping the qubits corresponding to 1 states
        
        
# # Making and connecting the agents 
# out = Agent.shared_output()
# alice = Alice(qstream, out)
# bob = Bob(qstream, out)
# alice.qconnect(bob) # adding a quantum channel
# alice.cconnect(bob) # adding a classical channel

# # Running everything 
# alice.start()
# bob.start()
# alice.join()
# bob.join()

# print("Teleported states {}".format(states_to_teleport))
# print("Received states   {}"). format(out["Bob"])




# angles = np.linspace(0, 2 * np.pi, 50)  # RX angles to apply
# num_trials = 250  # number of trials for each angle

# # Prepare the initial states in the stream
# qstream = QStream(3, len(angles) * num_trials)
# for angle in angles:
#     for _ in range(num_trials):
#         q, _, _ = qstream.next().qubits
#         RX(q, angle)

# # Make the agents and connect with quantum and classical channels
# out = Agent.shared_output()
# alice = Alice(qstream, out = out)
# bob = Bob(qstream, out = out)
# alice.qconnect(bob)
# alice.cconnect(bob)

# # Run the simulation
# Simulation(alice, bob).run()

# # Plot the results
# results = np.array(out["Bob"]).reshape((len(angles), num_trials))
# observed = np.mean(results, axis = 1)
# expected = np.sin(angles / 2) ** 2
# plt.plot(angles, observed, label = 'Observed')
# plt.plot(angles, expected, label = 'Expected')
# plt.legend()
# plt.xlabel("$\Theta$ in $R_X(\Theta)$ applied to qubits")
# plt.ylabel("Fractional $\left | 1 \\right >$ population")
# plt.show()