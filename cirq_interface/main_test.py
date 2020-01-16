import sys
sys.path.insert(0, '/home/alexandru/github/Intel-QS/build/lib')
import intelqs_py as simulator

import cirq

from intelqs_virtual_device import IntelQSVirtualDevice
from intelqs_simulator import IntelQSSimulator

print("Hello World! Intel QS")


qubit = cirq.NamedQubit("qubit")

circuit = cirq.Circuit(device=IntelQSVirtualDevice())

circuit.append(cirq.ops.H.on(qubit))
circuit.append(cirq.ops.H.on(qubit))


res = IntelQSSimulator().simulate(circuit)

print("Res", res)
