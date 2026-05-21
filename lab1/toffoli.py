from qiskit import QuantumCircuit as scheme
from qiskit import QuantumRegister as quantum_reg
from qiskit import ClassicalRegister as classical_reg
from qiskit.providers.basic_provider import BasicSimulator

print("1. Базовий приклад")
qc_basic = scheme(2, 2)
qc_basic.h(0)
qc_basic.cx(0, 1)
qc_basic.measure([0, 1], [0, 1])

simulator = BasicSimulator()
result_basic = simulator.run(qc_basic).result()
counts_basic = result_basic.get_counts(qc_basic)

print("Результати вимірювання стану Белла:", counts_basic)
print("\n" + "=" * 60 + "\n")

print("2. Вентиль Тоффолі та спрощенний вентиль Тоффолі")

qc_toffoli = scheme(3)
qc_toffoli.ccx(0, 1, 2)

qc_margolus = scheme(3)
qc_margolus.rccx(0, 1, 2)

print("Схема стандартного Тоффолі")
print(qc_toffoli.draw(output = 'text'))

print("\nСхема вентиля Марголуса")
print(qc_margolus.draw(output = 'text'))
print("\n" + "=" * 60 + "\n")

print("3. Додавання двох 4-бітних чисел")

def carry(qc, cin, a, b, cout):
    qc.ccx(a, b, cout)
    qc.cx(a, b)
    qc.ccx(cin, b, cout)

def reverse_carry(qc, cin, a, b, cout):
    qc.ccx(cin, b, cout)
    qc.cx(a, b)
    qc.ccx(a, b, cout)

def sum_gate(qc, cin, a, b):
    qc.cx(a, b)
    qc.cx(cin, b)

reg_a = quantum_reg(4, 'a')
reg_b = quantum_reg(4, 'b')
reg_c = quantum_reg(4, 'c')
reg_cout = quantum_reg(1)
cr = classical_reg(5, 'result')

qc_adder = scheme(reg_c, reg_a, reg_b, reg_cout, cr)
qc_adder.x(reg_a[0])
qc_adder.x(reg_a[2])
qc_adder.x(reg_b[0])
qc_adder.x(reg_b[1])
qc_adder.x(reg_b[2])
qc_adder.barrier()

for i in range(3):
    carry(qc_adder, reg_c[i], reg_a[i], reg_b[i], reg_c[i+1])
carry(qc_adder, reg_c[3], reg_a[3], reg_b[3], reg_cout[0])
sum_gate(qc_adder, reg_c[3], reg_a[3], reg_b[3])

for i in range(2, -1, -1):
    reverse_carry(qc_adder, reg_c[i], reg_a[i], reg_b[i], reg_c[i+1])
sum_gate(qc_adder, reg_c[i], reg_a[i], reg_b[i])

qc_adder.barrier()

for i in range(4):
    qc_adder.measure(reg_b[i], cr[i])
qc_adder.measure(reg_cout[0], cr[4])

result_adder = simulator.run(qc_adder).result()
counts_adder = result_adder.get_counts(qc_adder)

print("Результат додавання A(5) + B(7) = 12: ")
print("Отримано стан (b3 b2 b1 b0): ", counts_adder)
print("у бінарних числах")