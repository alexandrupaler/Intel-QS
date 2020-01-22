import sys, os

import numpy as np

sys.path.insert(
    0, os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../'))

import cirq

from cirq_interface import IntelQSVirtualDevice
from cirq_interface import IntelQSSimulator

from cirq_interface.experimental import CXXGenerator

def main():

    # print("Hello World! Intel QS")

    qubit0 = cirq.NamedQubit("qubit0")
    qubit1 = cirq.NamedQubit("qubit1")

    circuit = cirq.Circuit(device=IntelQSVirtualDevice())

    circuit.append(cirq.ops.H.on(qubit0))
    # circuit.append(cirq.ops.CNOT.on(qubit0, qubit1))
    # circuit.append(cirq.ops.Rx(np.pi * 0.5).on(qubit1))
    circuit.append(cirq.ops.Rz(np.pi * 0.5).on(qubit0))

    # print(circuit)

    # res = IntelQSSimulator().simulate(circuit)

    CXXGenerator(circuit)

    # print("Res", res)

if __name__ == "__main__":
    main()