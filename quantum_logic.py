# quantum_logic.py

from qiskit import QuantumCircuit, execute
from qiskit.providers.aer import AerSimulator
import random
import string

def generate_quantum_code(length=6):
    """Generate a quantum random code for short URLs"""
    # Simple pseudo-quantum randomness using random module
    # (For actual quantum randomness, you'd use a quantum backend)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def run_quantum_circuit():
    """Example function to demonstrate a quantum circuit on Render"""
    # Create a 1-qubit circuit
    qc = QuantumCircuit(1, 1)
    qc.h(0)          # Apply Hadamard gate to put qubit in superposition
    qc.measure(0, 0) # Measure the qubit

    # Use AerSimulator instead of Aer.get_backend
    simulator = AerSimulator()
    result = execute(qc, simulator, shots=1024).result()
    counts = result.get_counts()
    return counts
