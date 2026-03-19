import matplotlib.pyplot as plt; plt.rcParams.update({"font.family": "serif"})
import numpy as np
import pickle

import openfermion as of

import qiskit
from qiskit import qasm2, qasm3
from qiskit_aer import AerSimulator
import qiskit_ibm_runtime
from qiskit_ibm_runtime import SamplerV2 as Sampler
from remove_idle import remove_idle

fragment = "atp_0_be2_f14"

adapt_iterations: int = 10
circuit_dir =  "circuits/truncated_pool"
circuit_fname = f"{fragment}_{adapt_iterations:03d}_adaptiterations.qasm"
circuit_path = f"{circuit_dir}/{fragment}/{circuit_fname}"
circuit = qasm3.load(circuit_path)


qubits_to_bools, circuit = remove_idle(circuit)
print(qubits_to_bools)