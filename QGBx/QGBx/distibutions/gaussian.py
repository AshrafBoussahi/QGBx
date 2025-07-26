from ..base.distribution import Distribution
from ..base.device import Device
import pennylane as qml
import numpy as np

class Gaussian(Distribution):

    def __init__(self, device , **kwargs):
        super().__init__(device, "Gaussian", **kwargs)
        self.number_of_layers = 0
        
        

    def circuit(self, n_layers):

        n = n_layers
        self.number_of_layers = n
        num_qubits = 2 * (n + 1)
        control_qubit = 0
        ball_qubit = n + 1

         
        ball_measure_wires = [ball_qubit + i for i in range(-n, n+1, 2)]

        def peg(i):
                qml.CSWAP(wires=[control_qubit, i, i - 1])
                qml.CNOT(wires=[i, control_qubit])
                qml.CSWAP(wires=[control_qubit, i, i + 1])

        

        @qml.qnode(self.dev(wires=num_qubits))
        def gaussianCircuit():
            
            
            qml.Hadamard(wires=control_qubit)
            qml.PauliX(wires=ball_qubit)


            for layer in range(n):

                offset = layer
                positions = []
                for pos in range(-offset, offset + 1, 2):
                    i = ball_qubit + pos
                    if 0 < i < num_qubits - 1:
                        positions.append(i)


                for j, i in enumerate(positions):
                    peg(i)
                    if j < len(positions) - 1:
                        qml.CNOT(wires=[i + 1, control_qubit])


                if layer < n - 1:
                    m = qml.measure(wires=control_qubit)
                    qml.cond(m, qml.PauliX)(wires=control_qubit)
                    qml.Hadamard(wires=control_qubit)

            return qml.sample(wires=ball_measure_wires)
            
        return gaussianCircuit, ball_measure_wires
    
    def as_code(self):
        n = self.number_of_layers
        num_qubits = 2 * (n + 1)
        control_qubit = 0
        ball_qubit = n + 1

                
        #import pennylane as qml

        ####### initializin
        




    def ideal_distribution(self, **kwargs) :
        """Returns a discrete Gaussian-shaped distribution centered around the middle index."""
        n = 2 ** 4
        x = np.linspace(0, n - 1, n)
        mu = kwargs.get("mu", (n - 1) / 2)
        sigma = kwargs.get("sigma", n / 6)

        probs = np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        return probs / np.sum(probs)
    
    
    def as_code(self, n_layers: int) -> str:
        
        return f'''\
    @qml.qnode(qml.device("default.qubit", wires={2*(n_layers+1)}, shots=1000))
    def gaussianCircuit():
        control_qubit = 0
        ball_qubit = {n_layers + 1}
        ball_measure_wires = [ball_qubit + i for i in range(-{n_layers}, {n_layers}+1, 2)]

        def peg(i):
            qml.CSWAP(wires=[control_qubit, i, i - 1])
            qml.CNOT(wires=[i, control_qubit])
            qml.CSWAP(wires=[control_qubit, i, i + 1])

        qml.Hadamard(wires=control_qubit)
        qml.PauliX(wires=ball_qubit)

        for layer in range({n_layers}):
            offset = layer
            positions = []
            for pos in range(-offset, offset + 1, 2):
                i = ball_qubit + pos
                if 0 < i < {2*(n_layers+1)} - 1:
                    positions.append(i)

            for j, i in enumerate(positions):
                peg(i)
                if j < len(positions) - 1:
                    qml.CNOT(wires=[i + 1, control_qubit])

            if layer < {n_layers} - 1:
                m = qml.measure(wires=control_qubit)
                qml.cond(m, qml.PauliX)(wires=control_qubit)
                qml.Hadamard(wires=control_qubit)

        return qml.sample(wires=ball_measure_wires)
    '''
