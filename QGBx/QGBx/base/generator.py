import pennylane as qml
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from .device import Device
from .distribution import Distribution


# mypackage/module1.py
""" 
def greet(name):
    return f"Hello, {name}!"

def square(x):
    return x * x
 """




class Generator:


    def __init__(
        self,
        device: Device,
        #shots,
        distribution: Distribution,
        export_circuit_py = False,
        path = None,
        loop_in_code = False,
        export_circuit_png = False
        ):

        self.device = device
        self.exp_py = export_circuit_py
        #self.shots = shots

        if not(loop_in_code) and export_circuit_py:
            raise("Export Circuit as a python file is disabled")
        else:
            self.loop = loop_in_code

        if distribution.name not in ["Gaussian", "Exponential", "Hadamard_QW", "Custom_Per_Layer", "Custom_Per_Peg"]:
            raise("Distribution not recognized")
        else:
            self.dist = distribution

        


    
    

    def galton_board(self, n_layers):

        n = n_layers

        if self.dist.name == "Gaussian":
            return self.dist.circuit(n)
        


        




        """ num_qubits = 2 * (n + 1)
        control_qubit = 0
        ball_qubit = n + 1
        

        if self.device.device_name in ["Gaussian", "Symmetric_Hadamard_QW","Asymmetric_L_Hadamard_QW","Asymmetric_R_Hadamard_QW"]:
        

            dev = self.device(num_qubits)



            # Ball could land on any qubit from (n+1 - n) to (n+1 + n) → [1, 2, ..., 2n+1]
            ball_measure_wires = [ball_qubit + i for i in range(-n, n+1, 2)]

            def peg(i):
                # Peg sequence: CSWAP(i-1), CNOT(i), CSWAP(i+1)
                qml.CSWAP(wires=[control_qubit, i, i - 1])
                #qml.Hadamard(wires=i-1)
                qml.CNOT(wires=[i, control_qubit])
                qml.CSWAP(wires=[control_qubit, i, i + 1])
                #qml.Hadamard(wires=control_qubit)

            if self.dist in [""]:

                @qml.qnode(dev)
                def circuit():
                    # Initialize control qubit and ball
                    #qml.S(wires=control_qubit)
                    
                    qml.Hadamard(wires=control_qubit)
                    #qml.S(wires=control_qubit)
                    qml.PauliX(wires=ball_qubit)
                    #qml.Hadamard(wires=ball_qubit)
                    for layer in range(n):
                        # Determine peg positions
                        offset = layer
                        positions = []
                        for pos in range(-offset, offset + 1, 2):
                            i = ball_qubit + pos
                            if 0 < i < num_qubits - 1:
                                positions.append(i)

                        # Apply pegs
                        for j, i in enumerate(positions):
                            peg(i)
                            if j < len(positions) - 1:
                                qml.CNOT(wires=[i + 1, control_qubit])

                        # Reset control qubit to |0⟩ and reapply Hadamard
                        if layer < n - 1:
                            m = qml.measure(wires=control_qubit)
                            qml.cond(m, qml.PauliX)(wires=control_qubit)
                            qml.Hadamard(wires=control_qubit)

                    # Measurement
                    return qml.sample(wires=ball_measure_wires)
                
                
            
                return circuit
            
            elif self.dist == "Symmetric_Hadamard_QW":
                @qml.qnode(dev)
                def circuit():
                    # Initialize control qubit and ball
                    #qml.S(wires=control_qubit)
                    
                    qml.Hadamard(wires=control_qubit)
                    qml.S(wires=control_qubit)
                    qml.PauliX(wires=ball_qubit)
                    #qml.Hadamard(wires=ball_qubit)
                    for layer in range(n):
                        # Determine peg positions
                        offset = layer
                        positions = []
                        for pos in range(-offset, offset + 1, 2):
                            i = ball_qubit + pos
                            if 0 < i < num_qubits - 1:
                                positions.append(i)

                        # Apply pegs
                        for j, i in enumerate(positions):
                            peg(i)
                            if j < len(positions) - 1:
                                qml.CNOT(wires=[i + 1, control_qubit])

                        # Reset control qubit to |0⟩ and reapply Hadamard
                        if layer < n - 1:
                            #m = qml.measure(wires=control_qubit)
                            #qml.cond(m, qml.PauliX)(wires=control_qubit)
                            qml.Hadamard(wires=control_qubit)

                    # Measurement
                    return qml.sample(wires=ball_measure_wires)
                
                
            
                return circuit """


            
            
            







   
            # Draw circuit

