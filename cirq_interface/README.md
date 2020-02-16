**HOWTOuse this kind of transpiler**

*Step 1:* Compile InteQS using the instructions provided in the 
root directory.

The most important thing is to successfully compile the dynamic library 
`intelqs_py.cpython...` in `build/lib`. That will allow to use the IntelQS as
a simulator.

*Step 2:* In the conda environment required for the compilation of IntelQS run
`pip install cirq`

*Step 3:* An example of how to use the Intel simulator see 
`cirq_interface/main_test.py`.

*Step 4_Test:* Test if the output includes all the gates from the circuit
`python cirq_interface/main_test.py | grep "_CXX_NO_CLUE_"`
 and if the grep does not find anything, this is a clue that a valid CPP could
 be generated.

*Step 4_Run:* Write the generated experimental CPP into a file
`python cirq_interface/main_test.py > ../examples/google_cirq.cpp`

*Step 5:* Place `google_cirq.cpp` in the CMakeLists of examples, and then first
`cd build` followed by `make`.

*Note*: This should compile the translated circuit into a Intel-QS executable.
In this branch the Makefile is already edited, so warnings and errors like the 
following indicate that something is wrong with the generated file

```
/home/alexandru/github/Intel-QS/examples/google_cirq.cpp:2:1: warning: missing terminating " character
 "
 ^
/home/alexandru/github/Intel-QS/examples/google_cirq.cpp:2:1: error: missing terminating " character

```