import numpy as np
import random
from math import gcd
from fractions import Fraction as frac
from qiskit import QuantumCircuit as circuit
from qiskit import transpile
from qiskit.providers.basic_provider import BasicSimulator
from qiskit.visualization import plot_histogram

simulator = BasicSimulator()

def mod15(a, power):
    if a not in [2, 4, 7, 8, 11, 13, 14]:
        raise ValueError("a має бути взаємно простим з 15 і != 1")
        
    qc = circuit(4)
    
    if a == 2:
        if power == 0: qc.swap(0, 1); qc.swap(1, 2); qc.swap(2, 3)
        if power == 1: qc.swap(0, 2); qc.swap(1, 3) 
        if power == 2: pass 
    elif a == 7:
        if power == 0: qc.swap(2, 3); qc.swap(1, 2); qc.swap(0, 1); qc.x([0, 1, 2, 3])
        if power == 1: qc.swap(0, 2); qc.swap(1, 3)
        if power == 2: pass
    elif a == 8:
        if power == 0: qc.swap(2, 3); qc.swap(1, 2); qc.swap(0, 1)
        if power == 1: qc.swap(0, 2); qc.swap(1, 3)
        if power == 2: pass
    elif a == 11:
        if power == 0: qc.swap(0, 2); qc.swap(1, 3)
        if power == 1: pass
        if power == 2: pass
    elif a == 13:
        if power == 0: qc.swap(0, 1); qc.swap(1, 2); qc.swap(2, 3); qc.x([0, 1, 2, 3])
        if power == 1: qc.swap(0, 2); qc.swap(1, 3)
        if power == 2: pass
    elif a == 4:
        if power == 0: qc.swap(0, 2); qc.swap(1, 3)
        if power == 1: pass
        if power == 2: pass
    elif a == 14:
        if power == 0: qc.x([0, 1, 2, 3])
        if power == 1: pass
        if power == 2: pass

   
    U = qc.to_gate()
    U.name = f"{a} ^ {2**power} mod 15"
    c_U = U.control()
    return c_U


def inverse(n):
    qc = circuit(n)
    for qubit in range(n // 2):
        qc.swap(qubit, n - qubit - 1)
    for j in range(n):
        for m in range(j):
            qc.cp(-np.pi / float(2**(j - m)), m, j)
        qc.h(j)
    qc.name = "field"
    return qc

def period(a, N = 15):
    count_qubits = 3  
    data = 4
    
    qc = circuit(count_qubits + data, count_qubits)
    for q in range(count_qubits):
        qc.h(q)
        
    qc.x(count_qubits)

    for q in range(count_qubits):
        qc.append(mod15(a, q), [q] + list(range(count_qubits, count_qubits + data)))
    qc.append(inverse(count_qubits), range(count_qubits))
    qc.measure(range(count_qubits), range(count_qubits))
    
    return qc

N = 15
candidates = [2, 4, 7, 8, 11, 13, 14]
chosen_numbers = random.sample(candidates, 3)

print(f"Алгоритм Шора для модулю N = {N}\n")
print(f"Випадково обрані числа для пошуку періоду: {chosen_numbers}\n")

for a in chosen_numbers:
    print(f"Аналіз числа a = {a}")
    qc = period(a, N)
    t_circuit = transpile(qc, simulator)
    result = simulator.run(t_circuit, shots = 1024).result()
    counts = result.get_counts()
    detected_periods = set()
    
    for measured_value in counts:
        decimal = int(measured_value, 2)
        phase = decimal / 8 
        
        if phase > 0:
            fraction = frac(phase).limit_denominator(N)
            r = fraction.denominator
            if pow(a, r, N) == 1:
                detected_periods.add(r)

    if not detected_periods:
        print(f"Помилка, схема не має бути тривіальною\n")
    else:
        actual_r = min(detected_periods)
        print(f"Знайдений період r = {actual_r}; квантові виміри вказують на: {list(detected_periods)}")
        print(f"Перевірка: {a} ^ {actual_r} mod 15 = {pow(a, actual_r, 15)}")
    print("-" * 40)