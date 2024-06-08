# Programa que demuestra accesos a memoria

.data
array: .word 1, 2, 3, 4, 5  # Define un arreglo de 5 enteros

.text
.global _start

_start:
    la t0, array          # Carga la dirección base del array en el registro t0
    lw t1, 0(t0)          # Carga el primer elemento del array en t1 (acceso a memoria)
    lw t2, 4(t0)          # Carga el segundo elemento del array en t2 (acceso a memoria)
    lw t3, 8(t0)          # Carga el tercer elemento del array en t3 (acceso a memoria)
    lw t4, 12(t0)         # Carga el cuarto elemento del array en t4 (acceso a memoria)
    lw t5, 16(t0)         # Carga el quinto elemento del array en t5 (acceso a memoria)
    add t6, t1, t2        # Suma de registros (operación entre registros)
    sw t6, 0(t0)          # Almacena el resultado en la primera posición del array (acceso a memoria)

# Total de accesos a memoria: 6 (5 lecturas + 1 escritura)