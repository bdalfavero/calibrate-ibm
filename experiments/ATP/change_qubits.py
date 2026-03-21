from typing import List, Dict
import qiskit
from qiskit.circuit import QuantumRegister, Qubit

def qubits_from_regsiter(register: QuantumRegister) -> List[Qubit]:
    # For some reason the QuantumRegister object doesn't have an accessible
    # ._bits attribute. Can't figure this out, since the base class does have ._bits...
    dummy_ckt = qiskit.QuantumCircuit(register)
    return dummy_ckt.qubits


def map_qubits(circuit: qiskit.QuantumCircuit, qubit_map: Dict[Qubit, Qubit]) -> qiskit.QuantumCircuit:
    new_qs = list(qubit_map.values())
    new_circuit = qiskit.QuantumCircuit(new_qs)
    for inst in circuit.data:
        new_inst_qs = [qubit_map[q] for q in inst.qubits]
        new_circuit.append(inst.operation, new_inst_qs)
    return new_circuit

if __name__ == "__main__":
    qr1 = qiskit.circuit.QuantumRegister(2)
    qr2 = qiskit.circuit.QuantumRegister(2)
    qr1_qubits = qubits_from_regsiter(qr1)
    qr2_qubits = qubits_from_regsiter(qr2)
    print(qr1_qubits)
    print(qr2_qubits)

    ckt = qiskit.QuantumCircuit(qr1)
    ckt.cx(0, 1)
    ckt.h(1)
    print(ckt.qubits)
    qubit_map = dict(zip(qr1_qubits, qr2_qubits))
    new_ckt = map_qubits(ckt, qubit_map)
    print(new_ckt)
    print(new_ckt.qubits)