# Operaciones entre registros

.text
.global _start

_start:
    li t0, 5              # Carga el valor 5 en t0
    li t1, 10             # Carga el valor 10 en t1
    add t2, t0, t1        # Suma t0 y t1, guarda el resultado en t2
    sub t3, t1, t0        # Resta t0 de t1, guarda el resultado en t3
    and t4, t0, t1        # AND bit a bit entre t0 y t1, guarda el resultado en t4
    or t5, t0, t1         # OR bit a bit entre t0 y t1, guarda el resultado en t5
    xor t6, t0, t1        # XOR bit a bit entre t0 y t1, guarda el resultado en t6

# Total de operaciones entre registros: 5