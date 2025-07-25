from ..base.distribution import Distribution
from ..base.device import Device
import pennylane as qml
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

class HadamardQW(Distribution):

    def __init__(self, device, type = "Symmetric" , **kwargs):
        super().__init__(device, "Gaussian", **kwargs)
        if type not in ["Symmetric", "Asymmetric_Right", "Asymmetric_Left"]:
            raise("Unknown Type of Quantum Walk")
        else:
            self.type = type
        
        

        

    def circuit(self, n_layers):



        n = n_layers
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
            
            if self.type == "Asymmetric_Right":
                qml.PauliX(wires=control_qubit)

            qml.Hadamard(wires=control_qubit)

            if self.type == "Symmetric":
                qml.S(wires=control_qubit)


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
                    
                    qml.Hadamard(wires=control_qubit)

            return qml.sample(wires=ball_measure_wires)
        
        """ drawer = qml.draw_mpl(gaussianCircuit)
        drawer()
        plt.show()

        # Run circuit and get results
        res = gaussianCircuit()
        counts = Counter([tuple(sample) for sample in res])

        print("\nProbabilities (ball positions only):")
        for bitstring in range(2**len(ball_measure_wires)):
            bits = tuple(int(x) for x in format(bitstring, f'0{len(ball_measure_wires)}b'))
            prob = counts.get(bits, 0) / 1000
            print(f"{''.join(map(str, bits[::-1]))}: {prob:.3f}")

            # Post-process: compute probability for each measured wire
        position_probs = dict.fromkeys(ball_measure_wires, 0.0)

        for outcome, count in counts.items():
            for i, bit in enumerate(outcome):
                if bit == 1:
                    wire = ball_measure_wires[i]
                    position_probs[wire] += count

        # Normalize to get probabilities
        for k in position_probs:
            position_probs[k] /= 1000

        # Sort by wire index
        sorted_positions = sorted(position_probs.keys())
        sorted_probs = [position_probs[pos] for pos in sorted_positions]

        # Plot the result
        
        plt.figure(figsize=(8, 4))
        plt.bar([f'q{w}' for w in sorted_positions], sorted_probs, color='mediumblue')
        plt.xlabel('Qubit (Ball Position)')
        plt.ylabel('Probability')
        plt.title(f'Quantum Galton Board Probability Distribution (n={n})')
        plt.ylim(0, 1)
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.show()
        
            # Map qubit wires to integer positions
        position_map = {wire: i for i, wire in enumerate(sorted_positions)}
        position_probs_array = np.array([position_probs[wire] for wire in sorted_positions])

        # Define new discrete range (more bins than qubit positions)
        num_bins = 30  # Feel free to adjust
        new_range = np.linspace(0, len(sorted_positions) - 1, num_bins)

        # Interpolate probabilities onto new discrete bins
        interpolated_probs = np.interp(new_range, list(position_map.values()), position_probs_array)
        interpolated_probs /= np.sum(interpolated_probs)  # Re-normalize

        # Plot discrete bars with gaps
        plt.figure(figsize=(10, 4))
        bar_positions = np.arange(len(interpolated_probs))
        bar_width = 0.8  # < 1.0 to leave gaps

        plt.bar(bar_positions, interpolated_probs, width=bar_width, color='mediumblue', edgecolor='black')
        plt.xlabel('Discrete Interpolated Positions')
        plt.ylabel('Probability')
        plt.title(f'Spaced-Bar Quantum Galton Board Distribution (n={n})')
        plt.xticks(np.linspace(0, num_bins - 1, 7, dtype=int))  # reduce number of ticks
        plt.grid(axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show() """
                
                
            
        return gaussianCircuit




    def ideal_distribution(self, **kwargs) :
        """Returns a discrete Gaussian-shaped distribution centered around the middle index."""
        n = 2 ** 4
        x = np.linspace(0, n - 1, n)
        mu = kwargs.get("mu", (n - 1) / 2)
        sigma = kwargs.get("sigma", n / 6)

        probs = np.exp(-0.5 * ((x - mu) / sigma) ** 2)
        return probs / np.sum(probs)