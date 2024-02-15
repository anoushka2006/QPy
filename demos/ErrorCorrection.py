#from squanch import *
from scipy.stats import unitary_group
import copy
import numpy as np
import matplotlib.image as image
import matplotlib.pyplot as plt

from qpy.linalg import *
from qpy.gates import *
from qpy.measurement import *
from main import *

# from squanch import agent, channels, errors, qstream, qubit, simulate

class Alice(Agent):
        '''Alice sends an arbitrary Shor-encoded state to Bob'''
        def shor_encode(self, qsys):
                # psi is state to send, q1...q8 are ancillas from top to bottom in diagram
                psi, q1, q2, q3, q4, q5, q6, q7, q8 = qsys.qubits
                # Gates are enumerated left to right, top to bottom from figure
                cnot(psi, q3)
                cnot(psi, q6)
                H(psi)
                H(q3)
                H(q6)
                cnot(psi, q1)
                cnot(psi, q2)
                cnot(q3, q4)
                cnot(q3, q5)
                cnot(q6, q7)
                cnot(q6, q8)
                return psi, q1, q2, q3, q4, q5, q6, q7, q8

        def run(self):
                for qsys in self.qstream:
                        # send the encoded qubits to Bob
                        for qubit in self.shor_encode(qsys):
                                self.qsend(bob, qubit)
                                
class DumbAlice(Agent):
        "DumbAlice sends a state to Bob but forgets to error-correct!"
        def run(self):
            for qsys in self.qstream:
                    for qubit in qsys.qubits:
                             self.qsend(dumb_bob, qubit)
                
# Defining Bob's Behaviour                    
class Bob(Agent):
        "Bob receives Alice's qubits and applied error correction"
        def shor_decode(self, psi, q1, q2, q3, q4, q5, q6, q7, q8):
                # same enumeration as Alice
                cnot(psi, q1)
                cnot(psi, q2)
                TOFFOLI(q2, q1, psi)
                cnot(q3, q4)
                cnot(q3, q5)
                TOFFOLI(q5, q4, q3)
                cnot(q6, q7)
                cnot(q6, q8)
                TOFFOLI(q7, q8, q6) # Toffoli control qubit order doesn't matter
                H(psi)
                H(q3)
                H(q6)
                cnot(psi, q3)
                cnot(psi, q6)
                TOFFOLI(q6, q3, psi)
                return psi # psi is now Alice's original state


        def run(self):
            measurement_results = []
            for _ in self.qstream:
                        # Bob receives 9 qubits representing Alice's encoded state
                        received = [self.qrecv(alice) for _ in range(9)]
                        # Decode and measure the original state
                        psi_true = self.shor_decode(*received)
                        measurement_results.append(psi_true.measure())
            self.output(measurement_results)
                
                
class DumbBob(Agent):
        "DumbBob receives a state from Alice but does not error-correct"
        def run(self):
                measurement_results = []
                for _ in self.qstream:
                        received = [self.qrecv(dumb_alice) for _ in range(9)]
                        psi_true = received[0]
                        measurement_results.append(psi_true.measure())
                self.output(measurement_results)
            
               
class ShorError(QError):
        def __init__(self, qchannel):
                '''
                Instatiate the error model from the parent class
                :param QChannel qchannel: parent quantum channel
                '''
                QError.__init__(self, qchannel)
                self.count = 0
                self.error_applied = False

        def apply(self, qubit):
                '''
                Apply a random unitary operation to one of the qubits in a set of 9
                :param Qubit qubit: qubit from quantum channel
                :return: either unchanged qubit or None
                '''
                # reset error for each group of 9 qubits
                if self.count == 0:
                        self.error_applied = False
                self.count = (self.count + 1) % 9
                # qubit could be None if combining with other error models, such as attenuation
                if not self.error_applied and qubit is not None:
                        if np.random.rand() < 0.5: # apply the error
                                random_unitary = unitary_group.rvs(2) # pick a random U(2) matrix
                                qubit.apply(random_unitary)
                                self.error_applied = True
                return qubit    
            
class ShorQChannel(QChannel):
        '''Represents a quantum channel with a Shor error applied'''

        def __init__(self, from_agent, to_agent):
                QChannel.__init__(self, from_agent, to_agent)
                # register the error model
                self.errors = [ShorError(self)]
                


# helper functions 
def to_bits(string):
        '''Convert a string to a list of bits'''
        result = []
        for c in string:
                bits = bin(ord(c))[2:]
                bits = '00000000'[len(bits):] + bits
                result.extend([int(b) for b in bits])
        return result

def from_bits(bits):
        '''Convert a list of bits to a string'''
        chars = []
        for b in range(int(len(bits) / 8)):
                byte = bits[b*8:(b+1)*8]
                chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return ''.join(chars)
    

    # Prepare a message to send
    msg = "Peter Shor once lived in Ruddock 238! But who was Airman?"
    bits = to_bits(msg)

    # Encode the message as spin eigenstates
qstream = QStream(9, len(bits)) # 9 qubits per encoded state
for bit, qsystem in zip(bits, qstream):
    if bit == 1:
        X(qsystem.qubit(0))
        

# Alice and Bob will use error correction
out = Agent.shared_output()
alice = Alice(qstream, out)
bob = Bob(qstream, out)
alice.qconnect(bob, ShorQChannel)

# Dumb agents won't use error correction
qstream2 = copy.deepcopy(qstream)
dumb_alice = DumbAlice(qstream2, out)
dumb_bob = DumbBob(qstream2, out)
dumb_alice.qconnect(dumb_bob, ShorQChannel)



# running the simulation 
Simulation(dumb_alice, dumb_bob, alice, bob).run()

print("DumbAlice sent:   {}".format(msg))
print("DumbBob received: {}".format(from_bits(out["DumbBob"])))
print("Alice sent:       {}".format(msg))
print("Bob received:     {}".format(from_bits(out["Bob"])))

