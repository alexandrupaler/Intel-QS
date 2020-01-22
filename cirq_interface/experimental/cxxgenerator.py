import cirq

class CXXGenerator():

    def __init__(self, circuit):

        print("/* Hello World */")

        self.introduction_code(circuit)

        self.generate_cxx_from_cirq_circuit(circuit)

        self.conclusion_code()

    def introduction_code(self, circuit):
        print("#include \"../qureg/qureg.hpp\"")

        print("""
int main(int argc, char **argv)
{
#ifndef INTELQS_HAS_MPI
   std::cout << \"\\nThis introductory code is thought to be run with MPI.\\n\"
   << \"To do so, please set the option '-DIqsMPI=ON' when calling CMake.\\n\\n\"
   << \"However the code will execute also without MPI.\\n\\n\";
#endif
    // Create the MPI environment, passing the same argument to all the ranks.
    qhipster::mpi::Environment env(argc, argv);
    if (env.IsUsefulRank() == false) return 0;
    // int myid = env.GetStateRank();
""")
        print("""
    int num_qubits = {};""".format(len(circuit.all_qubits())))
        print("""
    std::size_t index = 0;
    QubitRegister<ComplexDP> psi (num_qubits, \"base\", index);
        """)


    def conclusion_code(self):

        print("""
    // There are 2^n amplitudes
    std::size_t num_amplitudes = UL(1L << UL(num_qubits));
    ComplexDP amplitude;
    std::stringstream buffer;
    buffer << \"\\nExplicit list of all amplitudes of |1000>:\\n\";
    for (index=0; index<num_amplitudes; ++index)
    {
        amplitude = psi.GetGlobalAmplitude(index);
        buffer << \"\tpsi(\" << index << \") = <\" << index << \"|psi> = \" << amplitude << \"\\n\";
    }
    qhipster::mpi::Print(buffer.str(),false);
    return 0;
}
""")


    def create_qubit_map(self, circuit):
        the_map = {}
        idx = 0
        for qubit in sorted(circuit.all_qubits()):
            the_map[qubit] = idx
            idx += 1
        return the_map


    def generate_cxx_from_cirq_circuit(self, circuit):

        qubit_map = self.create_qubit_map(circuit)

        for operation in circuit.all_operations():

            """
                Check if the gates are known single qubit gates
                If that is not the case then check 
                if it is a SingleQubitGate and obtain its unitary matrix
                that is passed to the simulator
            """
            if operation.gate == cirq.ops.H:
                print("""
    //Apply the Hadamard gate
    psi.ApplyHadamard({});""".format(qubit_map[operation.qubits[0]])
                      )

            # #
            # elif isinstance(operation.gate, cirq.ops.XPowGate):
            #     #
            #     # Rx, Rz, Ry are not classes but methods to create XPowGates
            #     # with global_shift = -0.5
            #     #
            #     print("apply rotation x")
            #     # current_qreg.ApplyRotationX(qubit_map[operation.qubits[0]],
            #     #                             operation.gate.exponent * np.pi)
            #
            # elif isinstance(operation.gate, cirq.ops.SingleQubitGate):
            #     # matrix = cirq.unitary(operation)
            #     # print(operation, matrix)
            #
            #     # current_qreg.Apply1QubitGate(qubit_map[operation.qubits[0]],
            #     #                              matrix)
            #
            # elif operation.gate == cirq.ops.CNOT:
            #     # current_qreg.ApplyCPauliX(qubit_map[operation.qubits[0]],
            #     #                           qubit_map[operation.qubits[1]])


