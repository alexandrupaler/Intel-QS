import cirq

class IntelQSVirtualDevice(cirq.Device):

    # def __init__(self, ):


    def duration_of(self, operation: 'cirq.Operation'):
        # No duration
        return 0

    def decompose_operation(self, operation):

        # Known gate name
        if not isinstance(operation, cirq.ops.GateOperation):
            raise TypeError("{!r} is not a gate operation.".format(operation))

        # default value
        decomposition = [operation]
        """
            Try to decompose the operation into elementary device operations
            TODO: Test how this works for different circuits
        """
        if not self.is_intelqs_virt_dev_op(operation):
            decomposition = cirq.decompose(operation,
                                           keep=self.is_intelqs_virt_dev_op)

        for dec in decomposition:
            if not self.is_intelqs_virt_dev_op(dec):
                raise TypeError("Don't know how to work with {!r}.".format(
                    operation.gate))

        return decomposition

    def is_intelqs_virt_dev_op(self, op):
        """
            This checks for the currently supported gate set
        """
        if not isinstance(op, cirq.ops.GateOperation):
            return False

        keep = False

        keep = keep or (isinstance(op.gate, cirq.ops.HPowGate) and
                        (op.gate.exponent == 1))

        keep = keep or (isinstance(op.gate, cirq.ops.CNotPowGate) and
                        (op.gate.exponent == 1))
        #
        # keep = keep or (isinstance(op.gate, ops.HPowGate) and
        #                 (op.gate.exponent == 1))
        #
        # keep = keep or (isinstance(op.gate, ops.XPowGate) and
        #                 (op.gate.exponent == 0.5))
        #
        # keep = keep or (isinstance(op.gate, ops.YPowGate) and
        #                 (op.gate.exponent == 0.5))
        #
        # keep = keep or (isinstance(op.gate, ops.ZPowGate) and
        #                 (op.gate.exponent == 0.25))
        #
        # keep = keep or (isinstance(op.gate, ops.ZPowGate))
        #
        # keep = keep or (isinstance(op.gate, ops.PhasedXPowGate) and
        #                 (op.gate.exponent == 0.5) and
        #                 (op.gate.phase_exponent == 0.25))
        #
        # keep = keep or (isinstance(op.gate, cirq.ops.FSimGate))

        return keep

    def validate_operation(self, operation):
        if not isinstance(operation, cirq.GateOperation):
            raise ValueError(
                '{!r} is not a supported operation'.format(operation))

        if not self.is_intelqs_virt_dev_op(operation):
            raise ValueError('{!r} is not a supported gate'.format(
                operation.gate))


    def validate_scheduled_operation(self, schedule, scheduled_operation):
        self.validate_operation(scheduled_operation.operation)

    def validate_circuit(self, circuit):
        #
        # Circuit and grid should have same number of qubits?
        # Otherwise -> Problem?
        #
        for moment in circuit:
            for operation in moment.operations:
                self.validate_operation(operation)

    def validate_schedule(self, schedule):
        for scheduled_operation in schedule.scheduled_operations:
            self.validate_scheduled_operation(schedule, scheduled_operation)
