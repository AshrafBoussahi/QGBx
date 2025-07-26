from .generator import Generator
from .runner import Runner
import matplotlib.pyplot as plt
import numpy as np

class Visualiser:
    def __init__(self, probs):
        self.probs = probs

    def plot_interpolated_distribution(self, num_bins=30):
        position_probs = {}
        for bits, prob in self.probs.items():
            idx = np.argmax(bits)
            position_probs[idx] = prob

        sorted_positions = sorted(position_probs.keys())
        position_map = {wire: i for i, wire in enumerate(sorted_positions)}
        position_probs_array = np.array([position_probs[wire] for wire in sorted_positions])

        new_range = np.linspace(0, len(sorted_positions) - 1, num_bins)
        interpolated_probs = np.interp(new_range, list(position_map.values()), position_probs_array)
        interpolated_probs /= np.sum(interpolated_probs)

        
        plt.figure(figsize=(10, 4))
        plt.bar(np.arange(num_bins), interpolated_probs, color='crimson')
        plt.xlabel('Interpolated Position')
        plt.ylabel('Probability')
        plt.title(f'Interpolated One-hot Distribution over {num_bins} Points')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.show()


    


