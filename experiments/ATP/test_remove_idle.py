import unittest
import numpy as np
import qiskit
from qiskit.quantum_info import Operator
from remove_idle import remove_idle, merge_idle_bits

class TestRemoveIdle(unittest.TestCase):

    def test_no_idle(self):
        ckt = qiskit.QuantumCircuit(3)
        ckt.cx(0, 1)
        ckt.cx(1, 2)
        ckt.cx(1, 0)
        _, removed_ckt = remove_idle(ckt)
        ckt_u = Operator(ckt).data
        removed_u = Operator(removed_ckt).data
        self.assertTrue(np.allclose(ckt_u, removed_u))

    def test_one_idle(self):
        ckt = qiskit.QuantumCircuit(3)
        ckt.cx(0, 2)
        ckt.cx(2, 0)
        ckt.x(1)
        _, removed_ckt = remove_idle(ckt)
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
        _, removed_ckt = remove_idle(ckt)
        target_ckt = qiskit.QuantumCircuit(2)
        target_ckt.h(0)
        target_ckt.cx(0, 1)
        target_ckt.cx(1, 0)
        target_u = Operator(target_ckt).data
        removed_u = Operator(removed_ckt).data
        self.assertTrue(np.allclose(target_u, removed_u))


class TestBools(unittest.TestCase):

    def test_no_idle(self):
        ckt = qiskit.QuantumCircuit(3)
        ckt.cx(0, 1)
        ckt.cx(1, 2)
        ckt.cx(1, 0)
        bools, _ = remove_idle(ckt)
        target_bools = {}
        self.assertTrue(bools == target_bools)

    def test_one_idle(self):
        ckt = qiskit.QuantumCircuit(3)
        ckt.cx(0, 2)
        ckt.cx(2, 0)
        ckt.x(1)
        bools, _ = remove_idle(ckt)
        target_bools = {1: True}
        self.assertTrue(target_bools == bools)

    def test_two_idle(self):
        ckt = qiskit.QuantumCircuit(4)
        ckt.h(3)
        ckt.h(0)
        ckt.cx(0, 2)
        ckt.cx(2, 0)
        ckt.x(1)
        bools, _ = remove_idle(ckt)
        target_bools = {1: True, 3: False}
        self.assertTrue(bools == target_bools)


class TestMergeIdle(unittest.TestCase):

    def test_one_idle(self):
        idle_bools = {1: False}
        active_inds = [0, 2]
        active_bools = np.array([
            [1, 0],
            [0, 1],
            [1, 1]
        ]).astype(bool)
        target_bools = np.array([
            [1, 0, 0],
            [0, 0, 1],
            [1, 0, 1]
        ]).astype(bool)
        merged_bools = merge_idle_bits(active_inds, active_bools, idle_bools)
        self.assertTrue(np.allclose(target_bools, merged_bools))

    def test_two_idle(self):
        idle_bools = {1: False, 3: True}
        active_inds = [0, 2]
        active_bools = np.array([
            [1, 0],
            [0, 1],
            [1, 1]
        ]).astype(bool)
        target_bools = np.array([
            [1, 0, 0, 1],
            [0, 0, 1, 1],
            [1, 0, 1, 1]
        ]).astype(bool)
        merged_bools = merge_idle_bits(active_inds, active_bools, idle_bools)
        self.assertTrue(np.allclose(target_bools, merged_bools))

if __name__ == "__main__":
    unittest.main()