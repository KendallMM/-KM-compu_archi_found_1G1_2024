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

    def memory_access(self):
        if self.IR.opcode == 'LOAD':
            self.MDR = self.memory[self.ALUOut]
        elif self.IR.opcode == 'STORE':
            self.memory[self.ALUOut] = self.B

    def write_back(self):
        if self.IR.opcode in ['ADD', 'SUB']:
            self.registers[self.IR.rd] = self.ALUOut
        elif self.IR.opcode == 'LOAD':
            self.registers[self.IR.rt] = self.MDR
        elif self.IR.opcode == 'JUMP':
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
(Instruction('JUMP', imm=1)),
]

# Establecer registros iniciales para la prueba
cpu.registers[1] = 10  # R1
cpu.registers[3] = 20  # R3
cpu.registers[5] = 30  # R5

# Establecer valores en memoria para la carga
cpu.memory[15] = 100  # Valor en la dirección 10 + 5

# Ejecuta las instrucciones en la CPU
for instr in instructions:
    cpu.memory[cpu.PC] = instr
    cpu.run_cycle()


# Mostrar el estado de los registros y memoria después de la ejecución
print("Registros:", cpu.registers)
print("Memoria (primeras 20 posiciones):", cpu.memory[:20])  # Mostrar primeras 20 posiciones de memoria
