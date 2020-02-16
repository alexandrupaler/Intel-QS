import sys, os

sys.path.insert(
    0, os.path.realpath(os.path.dirname(os.path.realpath(__file__)) + '/../'))

# import cirq
#
# from cirq_interface import IntelQSVirtualDevice
# from cirq_interface import IntelQSSimulator

import cirq.experiments as experiments

from cirq_interface.experimental import CXXGenerator

def main():

    # print("Hello World! Intel QS")

    supreme_circuit = experiments.generate_boixo_2018_supremacy_circuits_v2_bristlecone(
        # Do not exagerate with this parameter
        n_rows = 3,
        # Do not exagerate with this parameter
        cz_depth = 10,
        # Should be properly seeded
        seed = 0
    )

    # print(supreme_circuit)

    CXXGenerator(supreme_circuit)

if __name__ == "__main__":
    main()