import qiskit

def remove_idle(circuit: qiskit.QuantumCircuit) -> qiskit.QuantumCircuit:
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
    new_ckt = qiskit.QuantumCircuit(not_candidates)
    for inst in circuit.data:
        if len(set(inst.qubits) & set(candidates)) == 0:
            new_ckt.append(inst, inst.qubits)
    return new_ckt


if __name__ == "__main__":
    ckt = qiskit.QuantumCircuit(3)
    ckt.cx(0, 1)
    # ckt.cx(1, 2)
    new_ckt = remove_idle(ckt)
    print(ckt)
    print(new_ckt)
    print(new_ckt.qubits)