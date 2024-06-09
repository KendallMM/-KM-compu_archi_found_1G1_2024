class RegisterFile:
    def __init__(self):
        self.registers = [0] * 32

    def read(self, index):
        if index == 0:
            return 0
        return self.registers[index]

    def write(self, index, value):
        if index != 0:
            self.registers[index] = value

    def dump(self):
        return self.registers



class DataMemory:
    def __init__(self):
        self.memory = [0] * 1024  # Tamaño de la memoria en celdas (ajustar según necesidad)

    def read(self, address):
        return self.memory[address]

    def write(self, address, value):
        self.memory[address] = value

    def dump(self):
        return self.memory


class ControlUnit:
    def __init__(self):
        self.pc = 0

    def fetch(self, instruction_memory):
        if self.pc >= len(instruction_memory):
            return None  # No more instructions to fetch
        instruction = instruction_memory[self.pc]
        self.pc += 1
        return instruction

    def decode(self, instruction):
        if instruction is None:
            return None
        opcode = instruction & 0x7F
        rd = (instruction >> 7) & 0x1F
        funct3 = (instruction >> 12) & 0x7
        rs1 = (instruction >> 15) & 0x1F
        rs2 = (instruction >> 20) & 0x1F
        funct7 = (instruction >> 25) & 0x7F
        imm = (instruction >> 20) & 0xFFF  # Para tipo I (ADDI)
        return opcode, rd, funct3, rs1, rs2, funct7, imm

    def execute(self, opcode, rd, funct3, rs1, rs2, funct7, imm, register_file, data_memory):
        if opcode is None:
            return
        # Implementar operaciones de la ALU según el opcode y funct3
        if opcode == 0x33:  # Tipo R
            if funct3 == 0x0:  # ADD
                result = register_file.read(rs1) + register_file.read(rs2)
                register_file.write(rd, result)
        elif opcode == 0x13:  # Tipo I
            if funct3 == 0x0:  # ADDI
                result = register_file.read(rs1) + imm
                register_file.write(rd, result)

    def step(self, instruction_memory, register_file, data_memory):
        instruction = self.fetch(instruction_memory)
        if instruction is None:
            return False  # No more instructions to execute
        opcode, rd, funct3, rs1, rs2, funct7, imm = self.decode(instruction)
        self.execute(opcode, rd, funct3, rs1, rs2, funct7, imm, register_file, data_memory)
        self.print_state(instruction, opcode, rd, funct3, rs1, rs2, imm, register_file, data_memory)
        return True

    def print_state(self, instruction, opcode, rd, funct3, rs1, rs2, imm, register_file, data_memory):
        print(f"Instruction: 0x{instruction:08X}")
        print(f"Decoded: opcode=0x{opcode:02X}, rd=x{rd}, funct3=0x{funct3:X}, rs1=x{rs1}, rs2=x{rs2}, imm=0x{imm:X}")
        print(f"PC: {self.pc * 4}")
        print(f"Registers: {register_file.dump()}")
        print(f"Memory: {data_memory.dump()[:10]}")  # Limiting to first 10 memory cells for readability
        print("")

    def dump_state(self, register_file, data_memory):
        state = {
            "PC": self.pc * 4,
            "Registers": register_file.dump(),
            "Memory": data_memory.dump()
        }
        return state


def main():
    # Memoria de instrucciones (en hexadecimal)
    instruction_memory = [
        0x00A00513,  # ADDI x10, x0, 10
        0x00B505B3,  # ADD x11, x10, x11
        0x00000000  # NOP (para finalizar)
    ]

    # Inicializar componentes
    register_file = RegisterFile()
    data_memory = DataMemory()
    control_unit = ControlUnit()

    # Ejecutar programa
    while control_unit.step(instruction_memory, register_file, data_memory):
        pass

    # Mostrar estado final
    state = control_unit.dump_state(register_file, data_memory)
    print("Final State:")
    print(state)


if __name__ == "__main__":
    main()

