import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QComboBox, QTextEdit, QTableWidget, \
    QTableWidgetItem, QHBoxLayout, QSpinBox, QMessageBox, QGridLayout, QSizePolicy
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from multiciclo import MultiCycleCPU
from uniciclo import UniCycleCPU
import time

class CPUWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CPU Simulator")
        self.setFixedSize(1030, 715)
        self.prevCpu = None
        self.cpu = MultiCycleCPU()
        self.cpu.messageChanged.connect(self.update_output)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # ComboBox para seleccionar el tipo de procesador
        self.processor_combo = QComboBox(self)
        self.processor_combo.addItems(["Multiciclo", "Uniciclo"])
        layout.addWidget(self.processor_combo)

        # SpinBox para seleccionar el delay en centisegundos
        delay_layout = QHBoxLayout()
        self.delay_label = QLabel("Delay (ms):")
        delay_layout.addWidget(self.delay_label)
        self.delay_spinbox = QSpinBox(self)
        self.delay_spinbox.setRange(0, 1000)  # Rango de 0 a 1 segundo en centisegundos
        self.delay_spinbox.setValue(300)  # Valor por defecto: 0.1 segundo (10 centisegundos)
        delay_layout.addWidget(self.delay_spinbox)
        layout.addLayout(delay_layout)

        # SpinBox para seleccionar la cantidad de datos a mostrar de self.cpu.data_memory
        data_layout = QHBoxLayout()
        self.data_label = QLabel("Data Memory Size:")
        data_layout.addWidget(self.data_label)
        self.data_spinbox = QSpinBox(self)
        self.data_spinbox.setRange(0, 1024)  # Rango de 0 a 1024 (tamaño máximo de la memoria de datos)
        self.data_spinbox.setValue(27)  # Valor por defecto: 10 datos
        data_layout.addWidget(self.data_spinbox)
        layout.addLayout(data_layout)

        # Botones para controlar la ejecución
        self.start_button = QPushButton("Start Simulation")
        self.start_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Simulation")
        self.stop_button.clicked.connect(self.stop_simulation)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        self.step_button = QPushButton("Step-by-Step Execution")
        self.step_button.clicked.connect(self.run_step)
        layout.addWidget(self.step_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset)
        layout.addWidget(self.reset_button)

        # Layout for text areas
        text_area_layout = QGridLayout()
        layout.addLayout(text_area_layout)

        # Program Counter
        self.pc_label = QLabel("Program Counter:")
        text_area_layout.addWidget(self.pc_label, 0, 0)
        self.pc_text = QTextEdit(self)
        self.pc_text.setReadOnly(True)
        self.pc_text.setFixedWidth(300)
        self.pc_text.setFixedHeight(50)  # Adjust the height as needed
        text_area_layout.addWidget(self.pc_text, 1, 0)

        # FSM State
        self.fsm_label = QLabel("Ciclo de ejecución:")
        text_area_layout.addWidget(self.fsm_label, 0, 1)
        self.fsm_text = QTextEdit(self)
        self.fsm_text.setReadOnly(True)
        self.fsm_text.setFixedWidth(300)
        self.fsm_text.setFixedHeight(50)  # Adjust the height as needed
        text_area_layout.addWidget(self.fsm_text, 1, 1)

        # Memory and Registers
        self.memory_label = QLabel("Memory:")
        text_area_layout.addWidget(self.memory_label, 2, 0)
        self.memory_text = QTextEdit(self)
        self.memory_text.setReadOnly(True)
        self.memory_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        text_area_layout.addWidget(self.memory_text, 3, 0)
        self.memory_text.setFixedWidth(360)  # Adjust the height as needed

        self.registers_label = QLabel("Registers:")
        text_area_layout.addWidget(self.registers_label, 2, 1)
        self.registers_text = QTextEdit(self)
        self.registers_text.setReadOnly(True)
        self.registers_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        text_area_layout.addWidget(self.registers_text, 3, 1)
        self.registers_text.setFixedWidth(360)

        # Image
        self.image_label = QLabel(self)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        text_area_layout.addWidget(self.image_label, 0, 3, 0, 3)

        # Add image next to FSM state box
        image_path = "ProyectoGrupal2\\FSM_STATES\\MAQUINA.png"  # Replace with your image path

        if os.path.exists(image_path):
            self.image_label.setPixmap(QPixmap(image_path))
        else:
            QMessageBox.critical(self, "Error", f"Image file not found: {image_path}")
            # Optionally, set a default image or handle the missing file case
            self.image_label.setText("Image not found")

        # Tabla para mostrar el historial de ejecuciones
        self.table_label = QLabel("Ultimas 5 instrucciones:")
        text_area_layout.addWidget(self.table_label, 4, 0)
        self.history_table = QTableWidget(0, 7)
        self.history_table.setHorizontalHeaderLabels(["Procesador", "PC","Instrucción", "Ciclo", "Tiempo Total", "Latencia de instrucción", "CPI"])
        text_area_layout.addWidget(self.history_table, 5, 0, 1, 3)
        self.history_table.setFixedWidth(740)
        self.history_table.setFixedHeight(175)
        self.history_table.resizeColumnsToContents()

        self.execution_history = []  # Historial de ejecuciones
        self.execution_times = []  # List to store execution times

    def start_cpu(self):
        if self.processor_combo.currentText() == "Multiciclo":
            self.cpu = MultiCycleCPU()
            self.cpu.messageChanged.connect(self.update_output)
        elif self.processor_combo.currentText() == "Uniciclo":
            self.cpu = UniCycleCPU()
            self.cpu.messageChanged.connect(self.update_output)

    def start_simulation(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_cycle)
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.step_button.setEnabled(False)
        self.cpu.reset()
        delay = self.delay_spinbox.value()
        self.timer.start(delay)  # centisegundos
        
    def stop_simulation(self):
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.step_button.setEnabled(True)
        self.timer.stop()

    def run_cycle(self):
        if self.prevCpu != self.processor_combo.currentText():
            self.prevCpu = self.processor_combo.currentText()
            self.start_cpu()
        if not self.cpu:
            self.start_cpu()
        if not self.cpu.run_cycle():
            self.stop_simulation()
        self.update_status()

    def run_step(self):
        if self.prevCpu != self.processor_combo.currentText():
            self.prevCpu = self.processor_combo.currentText()
            self.start_cpu()
        if not self.cpu:
            self.start_cpu()
        if not self.cpu.run_cycle():
            self.step_button.setEnabled(False)
        self.update_status()

    def reset(self):
        if self.prevCpu != self.processor_combo.currentText():
            self.prevCpu = self.processor_combo.currentText()
            self.start_cpu()
        if self.start_button.isEnabled():
            self.step_button.setEnabled(True)
        self.cpu.reset()
        self.update_status()

    def update_output(self, message):
        self.pc_text.append(message)
        self.registers_text.append(message)
        self.memory_text.append(message)
        self.fsm_text.append(message)

        # Prevent auto-scroll up
        self.prevent_auto_scroll(self.pc_text)
        self.prevent_auto_scroll(self.registers_text)
        self.prevent_auto_scroll(self.memory_text)
        self.prevent_auto_scroll(self.fsm_text)

    def update_status(self):
        elapsed_time = time.time() - self.cpu.start_time if self.cpu.start_time else 0
        self.pc_text.setPlainText(f"PC: {self.cpu.PC}")
        self.registers_text.setPlainText(f"Registers: {self.cpu.registers}")
        data_memory_size = self.data_spinbox.value()
        self.memory_text.setPlainText(f"Memory: {self.cpu.data_memory[:data_memory_size]}")
        if self.processor_combo.currentText() == "Multiciclo":
            self.fsm_text.setPlainText(self.cpu.state)
            self.image_label.setPixmap(QPixmap(f"ProyectoGrupal2\\FSM_STATES\\{self.cpu.state}.png"))
        
        # Prevent auto-scroll up
        self.prevent_auto_scroll(self.pc_text)
        self.prevent_auto_scroll(self.registers_text)
        self.prevent_auto_scroll(self.memory_text)
        self.prevent_auto_scroll(self.fsm_text)
        
        self.log_execution(self.processor_combo.currentText())

    def prevent_auto_scroll(self, text_edit):
        cursor = text_edit.textCursor()
        cursor.movePosition(cursor.End)
        text_edit.setTextCursor(cursor)
        text_edit.ensureCursorVisible()

    def log_execution(self, processor_type):
        row_count = self.history_table.rowCount()
        self.history_table.insertRow(row_count)
        self.history_table.setItem(row_count, 0, QTableWidgetItem(processor_type))
        self.history_table.setItem(row_count, 1, QTableWidgetItem(str(self.cpu.PC)))
        self.history_table.setItem(row_count, 2, QTableWidgetItem(str(self.cpu.IR)))
        self.history_table.setItem(row_count, 3, QTableWidgetItem(str(self.cpu.Cycles)))

        current_time = time.time() - self.cpu.start_time
        self.history_table.setItem(row_count, 4, QTableWidgetItem(f"{current_time:.2f}s"))

        if self.execution_times:
            previous_time = self.execution_times[-1]
            latency_seconds = current_time - previous_time
            latency_ms = latency_seconds * 1000  # Convert seconds to milliseconds
        else:
            latency_ms = 0.0

        self.history_table.setItem(row_count, 5, QTableWidgetItem(f"{latency_ms:.2f}ms"))
        self.history_table.setItem(row_count, 6, QTableWidgetItem(str(self.cpu.CPI)[:5]))

        self.execution_history.append(
            (processor_type, self.cpu.PC, current_time, latency_ms))
        self.execution_times.append(current_time)
        self.history_table.resizeColumnsToContents()

        if len(self.execution_history) > 5:
            self.execution_history.pop(0)
            self.execution_times.pop(0)
            self.history_table.removeRow(0)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CPUWindow()
    window.show()
    sys.exit(app.exec_())

