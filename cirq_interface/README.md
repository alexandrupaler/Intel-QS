To use this interface:

Step 1: Compile InteQS using the instructions provided in the 
root directory.

The most important thing is to successfully compile the dynamic library 
`intelqs_py.cpython...` in `build/lib`. That will allow to use the IntelQS as
a simulator.

Step 2: In the conda environment required for the compilation of IntelQS run
`pip install cirq`

Step 3: An example of how to use the Intel simulator see `main_test.py`.