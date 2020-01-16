import sys, os

sys.path.insert(
    0, os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../'))

import cirq

from cirq_interface import IntelQSVirtualDevice
from cirq_interface import IntelQSSimulator


def main():

    print("Hello World! Intel QS")

    qubit0 = cirq.NamedQubit("qubit0")
    qubit1 = cirq.NamedQubit("qubit1")

    circuit = cirq.Circuit(device=IntelQSVirtualDevice())

    circuit.append(cirq.ops.H.on(qubit0))
    circuit.append(cirq.ops.CNOT.on(qubit0, qubit1))
    circuit.append(cirq.ops.XPowGate(exponent=0.5).on(qubit1))

    print(circuit)

    res = IntelQSSimulator().simulate(circuit)

    print("Res", res)

if __name__ == "__main__":
    main()