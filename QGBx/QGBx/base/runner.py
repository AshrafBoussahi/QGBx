from .generator import Generator
from collections import Counter
import pennylane as qml



class Runner:
    
    def __init__(self, generator:Generator):
        self.generator = generator


    def get_distribution(self):
        results = self.generator.gb()
        counts = Counter([tuple(sample) for sample in results])

        print("\nProbabilities of finding the ball at certain position:")
        one_hot_probs = {}
        num_shots = 1000
        n_wires = len(self.generator.measure_wires)

        for bitstring in range(2**n_wires):
            bits = tuple(int(x) for x in format(bitstring, f'0{n_wires}b'))
            if sum(bits) == 1:
                prob = counts.get(bits, 0) / num_shots
                one_hot_probs[bits] = prob
                #print(f"{''.join(map(str, bits[::-1]))}: {prob:.3f}")

        return one_hot_probs

