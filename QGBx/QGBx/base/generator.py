import pennylane as qml
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from .device import Device
from .distribution import Distribution
import inspect
import os


class Generator:


    def __init__(
        self,
        device: Device,
        distribution: Distribution,
        export_circuit_py = False,
        loop_in_code = False,
        export_circuit_png = False,
        path = None
        ):

        self.device = device
        self.exp_py = export_circuit_py
        self.path = path or "."
        self.n_layers = 0
        self.gb = None
        self.measure_wires = None

        if not(loop_in_code) and export_circuit_py:
            raise("Export Circuit as a python file is disabled")
        else:
            self.loop = loop_in_code

        if distribution.name not in ["Gaussian", "Exponential", "Hadamard_QW", "Custom_Per_Layer", "Custom_Per_Peg"]:
            raise("Distribution not recognized")
        else:
            self.dist = distribution   
    

    def galton_board(self, n_layers):

        #print(inspect.getsource(self.dist.circuit(n_layers)))
        self.n_layers = n_layers
        self.gb, self.measure_wires = self.dist.circuit(n_layers)


        return self.gb


    def export_circuit_as_png(self, filename: str = "circuit.png", style = "black_white"):

        if not self.path:
            raise RuntimeError("Exporting path is not defind in the Generator settings")

        qnode = self.galton_board(self.n_layers)

        try:
            fig, ax = qml.draw_mpl(qnode,style = style)()
            full_path = os.path.join(self.path, filename)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            fig.savefig(full_path)
            print(f"Circuit diagram exported to: {full_path}")
        except Exception as e:
            print("Failed to export circuit diagram:", e)

    
        
        
        


        


