from abc import ABC, abstractmethod
from .device import Device
import numpy as np

class Distribution(ABC):
    """
    Abstract base class for quantum distributions.
    
    Any subclass must implement:
    - a constructor taking device_name
    - a `circuit()` method defining the quantum circuit
    - an `ideal_distribution()` method returning the theoretical distribution
    """
    
    def __init__(self, device: Device, name: str, **kwargs):
        self.device_name = device.device_name
        self.name = name
        self.dev = device

    @abstractmethod
    def circuit(self, **kwargs):
        """Defines the quantum circuit for the distribution."""
        pass

    @abstractmethod
    def ideal_distribution(self, **kwargs):
        """
        Returns the ideal (theoretical) distribution as a NumPy array.
        
        Returns:
            np.ndarray: Theoretical distribution.
        """
        pass
