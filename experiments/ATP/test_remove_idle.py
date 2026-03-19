import unittest
import numpy as np
import qiskit
from qiskit.quantum_info import Operator
from remove_idle import remove_idle

class TestRemoveIdle(unittest.TestCase):

    def test_no_idle(self):
        ckt = qiskit.QuantumCircuit(3)
        ckt.cx(0, 1)
        ckt.cx(1, 2)
        ckt.cx(1, 0)
        removed_ckt = remove_idle(ckt)
        ckt_u = Operator(ckt).data
        removed_u = Operator(removed_ckt).data
        self.assertTrue(np.allclose(ckt_u, removed_u))

    def test_one_idle(self):
        ckt = qiskit.QuantumCircuit(3)
        ckt.cx(0, 2)
        ckt.cx(2, 0)
        ckt.x(1)
        removed_ckt = remove_idle(ckt)
        target_ckt = qiskit.QuantumCircuit(2)
        target_ckt.cx(0, 1)
        target_ckt.cx(1, 0)
        target_u = Operator(target_ckt).data
        removed_u = Operator(removed_ckt).data
        self.assertTrue(np.allclose(target_u, removed_u))

    def test_two_idle(self):
        ckt = qiskit.QuantumCircuit(4)
        ckt.h(3)
        ckt.h(0)
        ckt.cx(0, 2)
        ckt.cx(2, 0)
        ckt.x(1)
        removed_ckt = remove_idle(ckt)
        target_ckt = qiskit.QuantumCircuit(2)
        target_ckt.h(0)
        target_ckt.cx(0, 1)
        target_ckt.cx(1, 0)
        target_u = Operator(target_ckt).data
        removed_u = Operator(removed_ckt).data
        self.assertTrue(np.allclose(target_u, removed_u))

if __name__ == "__main__":
    unittest.main()