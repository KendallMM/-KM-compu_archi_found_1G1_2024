class Instruction:
    def __init__(self, opcode, rs=0, rt=0, rd=0, imm=0):
        self.opcode = opcode
        self.rs = rs
        self.rt = rt
        self.rd = rd
        self.imm = imm

    def __repr__(self):
        return f"Instruction(opcode='{self.opcode}', rs={self.rs}, rt={self.rt}, rd={self.rd}, imm={self.imm})"

class CPU:
    def __init__(self):
        self.registers = [0] * 32  # 32 registros
        self.memory = [0] * 1024  # Memoria de 1024 palabras
        self.PC = 0  # Contador de programa
        self.IR = None  # Registro de instrucción
        self.A = 0  # Registro A
        self.B = 0  # Registro B
        self.ALUOut = 0  # Salida de la ALU
        self.MDR = 0  # Registro de datos de memoria
        self.state = 'FETCH'  # Estado inicial de la FSM

    def fetch_instruction(self):
        self.IR = self.memory[self.PC]
        self.PC += 1

    def decode_instruction(self):
        self.A = self.registers[self.IR.rs]
        self.B = self.registers[self.IR.rt]

    def execute_instruction(self):
        if self.IR.opcode == 'ADD':
            self.ALUOut = self.A + self.B
        elif self.IR.opcode == 'SUB':
            self.ALUOut = self.A - self.B
        elif self.IR.opcode == 'LOAD':
            self.ALUOut = self.A + self.IR.imm
        elif self.IR.opcode == 'STORE':
            self.ALUOut = self.A + self.IR.imm
        elif self.IR.opcode == 'JUMP':
            self.ALUOut = self.PC + self.IR.imm
        elif self.IR.opcode == 'BEQ':
            if self.A == self.B:
                self.ALUOut = self.PC + self.IR.imm
            else:
                self.ALUOut = self.PC
        elif self.IR.opcode == 'AND':
            self.ALUOut = self.A & self.B
        elif self.IR.opcode == 'OR':
            self.ALUOut = self.A | self.B
        elif self.IR.opcode == 'XOR':
            self.ALUOut = self.A ^ self.B
        elif self.IR.opcode == 'SLT':
            self.ALUOut = 1 if self.A < self.B else 0
        elif self.IR.opcode == 'ADDI':
            self.ALUOut = self.A + self.IR.imm
        elif self.IR.opcode == 'SUBI':
            self.ALUOut = self.A - self.IR.imm
        elif self.IR.opcode == 'BNE':
            if self.A != self.B:
                self.ALUOut = self.PC + self.IR.imm
            else:
                self.ALUOut = self.PC

    def memory_access(self):
        if self.IR.opcode == 'LOAD':
            self.MDR = self.memory[self.ALUOut]
        elif self.IR.opcode == 'STORE':
            self.memory[self.ALUOut] = self.B

    def write_back(self):
        if self.IR.opcode in ['ADD', 'SUB','AND', 'OR', 'XOR', 'SLT']:
            self.registers[self.IR.rd] = self.ALUOut
        elif self.IR.opcode == 'LOAD':
            self.registers[self.IR.rt] = self.MDR
        elif self.IR.opcode == 'JUMP':
            self.PC = self.ALUOut
        elif self.IR.opcode == 'BEQ':
            self.PC = self.ALUOut
        elif self.IR.opcode == 'ADDI':
            self.registers[self.IR.rt] = self.ALUOut
        elif self.IR.opcode == 'SUBI':
            self.registers[self.IR.rt] = self.ALUOut
        elif self.IR.opcode == 'BNE':
            self.PC = self.ALUOut

    def run_cycle(self):
        if self.state == 'FETCH':
            self.fetch_instruction()
            print("State: FETCH")
            self.state = 'DECODE'
        elif self.state == 'DECODE':
            self.decode_instruction()
            print("State: DECODE")
            self.state = 'EXECUTE'
        elif self.state == 'EXECUTE':
            self.execute_instruction()
            if self.IR.opcode in ['LOAD', 'STORE']:
                self.state = 'MEMORY_ACCESS'
            else:
                self.state = 'WRITE_BACK'
            print("State: EXECUTE")
        elif self.state == 'MEMORY_ACCESS':
            self.memory_access()
            self.state = 'WRITE_BACK'
            print("State: MEMORY_ACCESS")
        elif self.state == 'WRITE_BACK':
            self.write_back()
            self.state = 'FETCH'
            print("State: WRITE_BACK")


    def print_memory(self, start=0, end=20):
        for i in range(start, end):
            if isinstance(self.memory[i], Instruction):
                print(f"Memory[{i}]: {self.memory[i]}")
            else:
                print(f"Memory[{i}]: {self.memory[i]}")

# Ejemplo de carga de instrucciones en memoria
cpu = CPU()
instructions = [
(Instruction('LOAD', rs=1, rt=2, imm=5)),
(Instruction('ADD', rs=2, rt=3, rd=4)),
(Instruction('STORE', rs=4, rt=5, imm=10)),
(Instruction('SUB', rs=4, rt=2, rd=1)),
(Instruction('BEQ', rs=1, rt=1, imm=2)),  # BEQ si rs == rt, salta 2 instrucciones adelante
(Instruction('ADD', rs=0, rt=0, rd=0)),   # Instrucción de relleno (no ejecutada si BEQ es exitoso)
(Instruction('JUMP', imm=1)),
(Instruction('AND', rs=2, rt=3, rd=7)),   # AND entre R2 y R3, resultado en R7
(Instruction('OR', rs=2, rt=3, rd=8)),    # OR entre R2 y R3, resultado en R8
(Instruction('XOR', rs=2, rt=3, rd=9)),   # XOR entre R2 y R3, resultado en R9
(Instruction('SLT', rs=2, rt=3, rd=10)),   # SLT entre R2 y R3, resultado en R10
(Instruction('ADDI', rs=2, rt=11, imm=10)), # ADDI suma 10 a R2 y almacena en R11
(Instruction('SUBI', rs=2, rt=12, imm=5)),  # SUBI resta 5 de R2 y almacena en R12
(Instruction('BNE', rs=1, rt=2, imm=2)), 
]

# Establecer registros iniciales para la prueba
cpu.registers[1] = 10  # R1
cpu.registers[3] = 20  # R3
cpu.registers[5] = 30  # R5

# Establecer valores en memoria para la carga
cpu.memory[15] = 100  # Valor en la dirección 10 + 5

# Cargar las instrucciones en memoria
for i, instr in enumerate(instructions):
    cpu.memory[i] = instr

# Ejecutar las instrucciones en la CPU
while cpu.PC-1 < len(instructions):
    while cpu.state != 'FETCH' or cpu.PC == 0:
        cpu.run_cycle()
    cpu.run_cycle()  # Ejecutar el ciclo FETCH para la próxima instrucción
    print(f"PC: {cpu.PC}")
    # print(f"len(instructions): {len(instructions)}")


# Mostrar el estado de los registros y memoria después de la ejecución
print("Registros:", cpu.registers)
print("Memoria (primeras 20 posiciones):", cpu.memory[:20])  # Mostrar primeras 20 posiciones de memoria
