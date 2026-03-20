from typing import Tuple, List, Dict
import qiskit
import numpy as np

def remove_idle(circuit: qiskit.QuantumCircuit) -> Tuple[qiskit.QuantumCircuit, Dict[int, bool]]:
    candidates = circuit.qubits.copy() # List of qubits that are not entangled with the "bulk".
    for inst in circuit.data:
        if len(inst.qubits) == 2:
            q1, q2 = inst.qubits
            if q1 in candidates:
                candidates.remove(q1)
            if q2 in candidates:
                candidates.remove(q2)
    candidates = sorted(candidates, key=lambda x: x._index)
    not_candidates = list(set(circuit.qubits) - set(candidates))
    not_candidates = sorted(not_candidates, key=lambda x: x._index)

    qubits_to_bools = {}
    for inst in circuit.data:
        if len(set(inst.qubits) & set(candidates)) != 0:
            if inst.name == 'x':
                qubits_to_bools[inst.qubits[0]._index] = True
    for candidate in candidates:
        if candidate._index not in qubits_to_bools.keys():
            qubits_to_bools[candidate._index] = False

    new_ckt = qiskit.QuantumCircuit(not_candidates)
    for inst in circuit.data:
        if len(set(inst.qubits) & set(candidates)) == 0:
            new_ckt.append(inst, inst.qubits)
    return qubits_to_bools, new_ckt


def merge_idle_bits(active_inds: List[int], active_bools: np.ndarray, idle_bools: Dict[int, bool]) -> np.ndarray:
    """If some bits are predetermined, put them into the array in the proper order."""

    assert active_bools.shape[1] == len(active_inds)
    num_shots = active_bools.shape[0]
    idle_inds = sorted(list(idle_bools.keys()))
    assert len(set(active_inds) & set(idle_inds)) == 0
    all_inds = sorted(active_inds + idle_inds)

    all_bools = np.zeros((num_shots, len(all_inds))).astype(bool)
    for i in range(num_shots):
        for j, q in enumerate(all_inds):
            if q in active_inds:
                old_idx = active_inds.index(q)
                all_bools[i, j] = active_bools[i, old_idx]
            else:
                all_bools[i, j] = idle_bools[q]
    return all_bools

if __name__ == "__main__":
    ckt = qiskit.QuantumCircuit(3)
    ckt.cx(0, 1)
    # ckt.cx(1, 2)
    new_ckt = remove_idle(ckt)
    print(ckt)
    print(new_ckt)
    print(new_ckt.qubits)