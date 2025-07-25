import pennylane as qml


class Device:
    def __init__(self, device_name, shots):
        self.device_name = device_name
        self.shots = shots

    def __call__(self, wires):
        print("Working")
        return qml.device(self.device_name, wires=wires, shots=self.shots)
