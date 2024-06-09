class UnicycleProcessor:
    def __init__(self, instructions, memory):
        self.instructions = instructions
        self.memory = memory
        self.pc = 0  # Program Counter
        self.registers = [0] * 32  # 32 registros
        self.cycle_count = 0
        self.running = False

    def execute_step(self):
        if self.pc < len(self.instructions):
            instruction = self.instructions[self.pc]
            opcode = instruction[0]
            operands = instruction[1:]

            if opcode == "ADD":  # Ejemplo de operación: suma
                rd, rs1, rs2 = operands
                self.registers[rd] = self.registers[rs1] + self.registers[rs2]
            elif opcode == "MUL":  # Ejemplo de operación: multiplicación
                rd, rs1, rs2 = operands
                self.registers[rd] = self.registers[rs1] * self.registers[rs2]

            self.pc += 1
            self.cycle_count += 1
            return True
        else:
            self.running = False
            return False

    def execute_program(self):
        self.running = True
        while self.running:
            self.execute_step()

    def print_state(self):
        print("Cycle:", self.cycle_count)
        print("PC:", self.pc)
        print("Registers:", self.registers)
        print("Memory:", self.memory)

# Ejemplo de uso:
instructions = [("ADD", 1, 2, 3), ("MUL", 4, 5, 6)]  # Ejemplo de instrucciones
memory = [0] * 256  # Ejemplo de memoria
processor = UnicycleProcessor(instructions, memory)
processor.execute_program()
processor.print_state()
