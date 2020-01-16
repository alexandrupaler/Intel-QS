from typing import Union, Sequence, List, Any

import numpy as np
import cirq

from cirq import study, schedules, ops, circuits, SimulatesFinalState

import sys
sys.path.insert(0, '/home/alexandru/github/Intel-QS/build/lib')
import intelqs_py as intelqs_simulator

from intelqs_virtual_device import IntelQSVirtualDevice

class IntelQSSimulator(SimulatesFinalState):

    def __init__(self):
        return

    def simulate_sweep(
            self,
            program: Union[circuits.Circuit, schedules.Schedule],
            params: study.Sweepable,
            qubit_order: ops.QubitOrderOrList = ops.QubitOrder.DEFAULT,
            initial_state: Any = None,
    ) -> List['SimulationTrialResult']:

        # if not isinstance(program, IntelQSCircuit):
        #     raise ValueError('{!r} is not a IntelQSCircuit'.format(program))

        if not isinstance(program.device, IntelQSVirtualDevice):
            # The circuit was not validated against the device
            raise ValueError('{!r} is not a IntelQSVirtualDevice'.format(
                program.device))

        param_resolvers = study.to_resolvers(params)

        qubit_map = {
           cirq.NamedQubit('qubit') :0
        }

        trials_results = []
        for prs in param_resolvers:

            from cirq import protocols
            solved_circuit = protocols.resolve_parameters(program, prs)

            num_qubits = len(solved_circuit.all_qubits())

            current_qreg = intelqs_simulator.QubitRegister(num_qubits, "base", 0, 0)

            for operation in solved_circuit.all_operations():
                if (operation.gate == cirq.ops.H):
                    current_qreg.ApplyHadamard(0)

            ary = np.array([current_qreg[i] for i in range(current_qreg.GlobalSize())])
            current_res = cirq.WaveFunctionSimulatorState(
                ary,
                qubit_map= qubit_map)

            current_res.final_state = ary

            trials_results.append(current_res)

        return trials_results
