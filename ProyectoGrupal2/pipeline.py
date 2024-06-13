from PyQt5.QtCore import QThread, pyqtSignal
import time
from memory import *
class SegmentedPipelineCPU(QThread):
    # Señales para actualizar los mensajes y el estado del pipeline en la interfaz
    messageChanged = pyqtSignal(str)
    pipelineStateChanged = pyqtSignal(list)

    def __init__(self, cycleTime=1):
        super().__init__()
        self.cycleTime = cycleTime  # Tiempo de ciclo en segundos
        self.reset()  # Inicializar la CPU

    def reset(self):
        # Inicializa o reinicia los registros y la memoria
        self.start_time = time.time()
        self.registers = [0] * 32  # 32 registros inicializados a 0
        self.memory = [0] * 1024  # Memoria principal
        self.instruction_memory = [None] * 256  # Memoria de instrucciones
        combined_memory = Memory().combined_memory
        self.memory[:len(combined_memory)] = combined_memory
        self.data_memory = [0] * 1024  # Memoria de datos
        self.PC = 0  # Contador de programa
        self.IF_ID = None  # Registro entre etapas
        self.ID_EX = None
        self.EX_MEM = None
        self.MEM_WB = None
        self.instruction_count = self.separate_memory()  # Separar las instrucciones de los datos

    def fetch(self):
        # Busca una instrucción desde la memoria de instrucciones
        if self.PC >= self.instruction_count:
            return None
        instruction = self.instruction_memory[self.PC]
        self.PC += 1
        self.messageChanged.emit(f"Fetched: {instruction}")
        return instruction

    def decode(self, instruction):
        # Decodifica la instrucción y lee los registros correspondientes
        if not instruction:
            return None
        A = self.registers[instruction.rs]
        B = self.registers[instruction.rt]
        self.messageChanged.emit(f"Decoded: A = {A}, B = {B}")
        return (instruction, A, B)

    def execute(self, decoded):
        # Ejecuta la instrucción usando la ALU
        if not decoded:
            return None
        instruction, A, B = decoded
        ALUOut = 0
        if instruction.opcode == 'ADD':
            ALUOut = A + B
        elif instruction.opcode == 'SUB':
            ALUOut = A - B
        elif instruction.opcode == 'MUL':
            ALUOut = A * B
        elif instruction.opcode == 'LOAD':
            ALUOut = A + instruction.imm
        elif instruction.opcode == 'STORE':
            ALUOut = A + instruction.imm
        elif instruction.opcode == 'JUMP':
            ALUOut = self.PC + instruction.imm
        elif instruction.opcode == 'BEQ':
            ALUOut = self.PC + instruction.imm if A == B else self.PC
        elif instruction.opcode == 'AND':
            ALUOut = A & B
        elif instruction.opcode == 'OR':
            ALUOut = A | B
        elif instruction.opcode == 'XOR':
            ALUOut = A ^ B
        elif instruction.opcode == 'SLT':
            ALUOut = 1 if A < B else 0
        elif instruction.opcode == 'ADDI':
            ALUOut = A + instruction.imm
        elif instruction.opcode == 'SUBI':
            ALUOut = A - instruction.imm
        elif instruction.opcode == 'BNE':
            ALUOut = self.PC + instruction.imm if A != B else self.PC
        self.messageChanged.emit(f"Executed: ALUOut = {ALUOut}")
        return (instruction, ALUOut, B)

    def memory_access(self, executed):
        # Accede a la memoria de datos para LOAD y STORE
        if not executed:
            return None
        instruction, ALUOut, B = executed
        MDR = 0
        if instruction.opcode == 'LOAD':
            MDR = self.data_memory[ALUOut]
        elif instruction.opcode == 'STORE':
            self.data_memory[ALUOut] = B
        self.messageChanged.emit(f"Memory Access: MDR = {MDR}")
        return (instruction, ALUOut, MDR)

    def write_back(self, mem_accessed):
        # Escribe el resultado de vuelta en el registro correspondiente
        if not mem_accessed:
            return
        instruction, ALUOut, MDR = mem_accessed
        if instruction.opcode in ['ADD', 'SUB', 'AND', 'OR', 'XOR', 'SLT', 'MUL']:
            self.registers[instruction.rd] = ALUOut
        elif instruction.opcode == 'LOAD':
            self.registers[instruction.rt] = MDR
        elif instruction.opcode in ['JUMP', 'BEQ', 'BNE']:
            self.PC = ALUOut
        elif instruction.opcode in ['ADDI', 'SUBI']:
            self.registers[instruction.rt] = ALUOut
        self.messageChanged.emit(f"Write Back: Registers = {self.registers}")

    def run_cycle(self):
        # Ejecuta un ciclo del pipeline
        self.MEM_WB = self.memory_access(self.EX_MEM)
        self.write_back(self.MEM_WB)
        self.EX_MEM = self.execute(self.ID_EX)
        self.ID_EX = self.decode(self.IF_ID)
        self.IF_ID = self.fetch()

        # Emite la señal con el estado actual del pipeline
        pipeline_state = [self.IF_ID, self.ID_EX, self.EX_MEM, self.MEM_WB]
        self.pipelineStateChanged.emit(pipeline_state)

        # Verifica si todas las etapas están vacías para detener la ejecución
        if self.IF_ID is None and self.ID_EX is None and self.EX_MEM is None and self.MEM_WB is None:
            return False
        return True

    def run(self):
        # Ejecuta continuamente los ciclos del pipeline con el delay especificado
        while self.run_cycle():
            time.sleep(self.cycleTime)

    def separate_memory(self):
        # Separa las instrucciones de los datos en la memoria
        instruction_count = 0
        for i, entry in enumerate(self.memory):
            if isinstance(entry, Instruction):
                self.instruction_memory[instruction_count] = entry
                instruction_count += 1
            else:
                break
        for j in range(instruction_count, len(self.memory)):
            self.data_memory[j - instruction_count] = self.memory[j]
        return instruction_count

