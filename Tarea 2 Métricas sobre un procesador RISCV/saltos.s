# Programa que demuestra saltos
# Contador de 1 a 10 por medio de saltos

.text
.global _start

_start:
    li t0, 10             # Carga el valor 10 en t0
    li t1, 0              # Carga el valor 0 en t1
loop:
    beq t1, t0, end_loop  # Si t1 == t0, salta a end_loop (salto condicional)
    addi t1, t1, 1        # Incrementa t1 en 1 (operación entre registros)
    j loop                # Salta incondicionalmente a loop (salto incondicional)
end_loop:
    nop                   # No operación

# Total de saltos: 2 (1 condicional + 1 incondicional)