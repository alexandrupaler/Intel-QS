from typing import Union, List, Any

import numpy as np
import cirq

from build.lib import intelqs_py as intelqs_simulator

from cirq_interface import IntelQSVirtualDevice

class IntelQSSimulator(cirq.SimulatesFinalState):

    def __init__(self):
        return

    def create_qubit_map(self, circuit):
        the_map = {}
        idx = 0
        for qubit in sorted(circuit.all_qubits()):
            the_map[qubit] = idx
            idx += 1

        return the_map

    def simulate_sweep(
            self,
            program: Union[cirq.circuits.Circuit, cirq.schedules.Schedule],
            params: cirq.study.Sweepable,
            qubit_order: cirq.ops.QubitOrderOrList = cirq.ops.QubitOrder.DEFAULT,
            initial_state: Any = None,
    ) -> List['SimulationTrialResult']:

        # if not isinstance(program, IntelQSCircuit):
        #     raise ValueError('{!r} is not a IntelQSCircuit'.format(program))

        if not isinstance(program.device, IntelQSVirtualDevice):
            # The circuit was not validated against the device
            raise ValueError('{!r} is not a IntelQSVirtualDevice'.format(
                program.device))

        param_resolvers = cirq.study.to_resolvers(params)

        qubit_map = self.create_qubit_map(program)

        trials_results = []

        for prs in param_resolvers:

            from cirq import protocols
            solved_circuit = protocols.resolve_parameters(program, prs)

            num_qubits = len(solved_circuit.all_qubits())

            current_qreg = intelqs_simulator.QubitRegister(num_qubits, "base", 0, 0)


            for moment in solved_circuit:
                for operation in moment:

                    """
                        Check if the gates are known single qubit gates
                        If that is not the case then check 
                        if it is a SingleQubitGate and obtain its unitary matrix
                        that is passed to the simulator
                    """
                    if operation.gate == cirq.ops.H:
                        current_qreg.ApplyHadamard(qubit_map[operation.qubits[0]])

                    #
                    elif isinstance(operation.gate, cirq.ops.XPowGate):
                        #
                        # Rx, Rz, Ry are not classes but methods to create XPowGates
                        # with global_shift = -0.5
                        #
                        print("apply rotation x")
                        current_qreg.ApplyRotationX(qubit_map[operation.qubits[0]],
                                                    operation.gate.exponent * np.pi)

                    elif isinstance(operation.gate, cirq.ops.SingleQubitGate):
                        matrix = cirq.unitary(operation)
                        print(operation, matrix)

                        current_qreg.Apply1QubitGate(qubit_map[operation.qubits[0]],
                                                     matrix)

                    elif operation.gate == cirq.ops.CNOT:
                        current_qreg.ApplyCPauliX(qubit_map[operation.qubits[0]],
                                                  qubit_map[operation.qubits[1]])

            ary = np.array([current_qreg[i] for i in range(current_qreg.GlobalSize())])
            current_res = cirq.WaveFunctionSimulatorState(
                ary,
                qubit_map= qubit_map)

            current_res.final_state = ary

            trials_results.append(current_res)

        return trials_results
