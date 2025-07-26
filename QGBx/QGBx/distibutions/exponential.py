from ..base.distribution import Distribution
from ..base.device import Device
import pennylane as qml
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class Exponential(Distribution):

    def __init__(self, device, **kwargs):
        super().__init__(device, "Exponential", **kwargs)
    
       
        
        

        

    def circuit(self, n_layers):
        def theta_decay(n, lam=2.0, max_angle=np.pi/2):
            x = np.arange(n)
            return max_angle * np.exp(-lam * x)
        n = n_layers
        num_qubits = 2 * (n + 1)
        control_qubit = 0
        ball_qubit = n + 1
        shots = 1000

        dev = qml.device("default.qubit", wires=num_qubits, shots=shots)

        ball_measure_wires = [ball_qubit + i for i in range(-n, n + 1, 2)]

        
        thetas = theta_decay(n, lam=2.0)

        def peg(i):
            qml.CSWAP(wires=[control_qubit, i, i - 1])
            qml.CNOT(wires=[i, control_qubit])
            qml.CSWAP(wires=[control_qubit, i, i + 1])

        @qml.qnode(dev)
        def ExponentialCircuit():
            qml.PauliX(wires=control_qubit)
            qml.PauliX(wires=ball_qubit)

            for layer in range(n):
                offset = layer
                positions = []
                for pos in range(-offset, offset + 1, 2):
                    i = ball_qubit + pos
                    if 0 < i < num_qubits - 1:
                        positions.append(i)

                # Apply Rx with decreasing θ → favors staying left
                qml.RX(thetas[layer], wires=control_qubit)

                for j, i in enumerate(positions):
                    peg(i)
                    if j < len(positions) - 1:
                        qml.CNOT(wires=[i + 1, control_qubit])

                # Reset control qubit
                if layer < n - 1:
                    m = qml.measure(wires=control_qubit)
                    qml.cond(m == 1, qml.PauliX)(wires=control_qubit)

            return qml.sample(wires=ball_measure_wires)

                    
        return ExponentialCircuit, ball_measure_wires




    def ideal_distribution(self, **kwargs) :
        """Returns a discrete Gaussian-shaped distribution centered around the middle index."""
        n = 2 ** 4
        x = np.linspace(0, n - 1, n)
        mu = kwargs.get("mu", (n - 1) / 2)
        sigma = kwargs.get("sigma", n / 6)

        probs = np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        return probs / np.sum(probs)