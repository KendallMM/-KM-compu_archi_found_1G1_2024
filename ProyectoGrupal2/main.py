import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QTextEdit, QLabel, QTableWidget, \
    QTableWidgetItem

class ProcessorSimulatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.processor = None
        self.execution_history = []  # Historial de ejecuciones
        self.initUI()

    def initUI(self):
        # Configuración de la interfaz gráfica
        self.setWindowTitle("Processor Simulator")

        layout = QVBoxLayout()

        # ComboBox para seleccionar el tipo de procesador
        self.processor_combo = QComboBox(self)
        self.processor_combo.addItems(
            ["Select Processor", "Uniciclo", "Multiciclo", "Segmentado con stalls", "Segmentado con adelantamiento"])
        layout.addWidget(self.processor_combo)

        # Botones para controlar la ejecución
        self.step_button = QPushButton("Step", self)
        self.step_button.clicked.connect(self.step)
        layout.addWidget(self.step_button)

        self.run_button = QPushButton("Run", self)
        self.run_button.clicked.connect(self.run)
        layout.addWidget(self.run_button)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset)
        layout.addWidget(self.reset_button)

        # Etiqueta y área de texto para mostrar el estado del procesador
        self.status_label = QLabel("Status:")
        layout.addWidget(self.status_label)

        self.status_text = QTextEdit(self)
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)

        # Tabla para mostrar el historial de ejecuciones
        self.history_table = QTableWidget(0, 3)
        self.history_table.setHorizontalHeaderLabels(["Processor", "Cycles", "Execution Time"])
        layout.addWidget(self.history_table)

        self.setLayout(layout)

    def step(self):
        # Ejecutar un paso del procesador según el tipo seleccionado
        processor_type = self.processor_combo.currentText()
        if processor_type == "Uniciclo":
            if not self.processor:
                self.processor = UnicicloProcessor()
            self.processor.step()
        elif processor_type == "Multiciclo":
            if not self.processor:
                self.processor = MulticicloProcessor()
            self.processor.step()
        elif "Segmentado" in processor_type:
            if not self.processor:
                self.processor = SegmentadoProcessor()
            self.processor.step()
        self.update_status()

    def run(self):
        # Ejecutar el programa completo según el tipo seleccionado
        processor_type = self.processor_combo.currentText()
        if processor_type == "Uniciclo":
            if not self.processor:
                self.processor = UnicicloProcessor()
            self.processor.run()
        elif processor_type == "Multiciclo":
            if not self.processor:
                self.processor = MulticicloProcessor()
            self.processor.run()
        elif "Segmentado" in processor_type:
            if not self.processor:
                self.processor = SegmentadoProcessor()
            self.processor.run()
        self.update_status()
        self.log_execution(processor_type)

    def reset(self):
        # Reiniciar el procesador y actualizar el estado
        self.processor = None
        self.update_status()

    def update_status(self):
        # Actualizar el estado del procesador en el área de texto
        if self.processor:
            elapsed_time = time.time() - self.processor.start_time if self.processor.start_time else 0
            status = f"PC: {self.processor.PC}\nRegisters: {self.processor.registers}\nMemory: {self.processor.memory[:10]}"  # Mostrar solo las primeras 10 posiciones de memoria
            status += f"\nCycles: {self.processor.cycle_count}\nExecution Time: {elapsed_time:.2f}s"
            if isinstance(self.processor, MulticicloProcessor):
                status += f"\nFSM State: {self.processor.state}"
            elif isinstance(self.processor, SegmentadoProcessor):
                pipeline_status = "\nPipeline:"
                for stage, instruction in self.processor.pipeline.items():
                    pipeline_status += f"\n{stage}: {instruction}"
                status += pipeline_status
            self.status_text.setText(status)
        else:
            self.status_text.setText("Processor not initialized.")

    def log_execution(self, processor_type):
        # Registrar la ejecución en el historial
        row_count = self.history_table.rowCount()
        self.history_table.insertRow(row_count)
        self.history_table.setItem(row_count, 0, QTableWidgetItem(processor_type))
        self.history_table.setItem(row_count, 1, QTableWidgetItem(str(self.processor.cycle_count)))
        self.history_table.setItem(row_count, 2, QTableWidgetItem(f"{time.time() - self.processor.start_time:.2f}s"))

        self.execution_history.append(
            (processor_type, self.processor.cycle_count, time.time() - self.processor.start_time))
        if len(self.execution_history) > 5:
            self.execution_history.pop(0)
            self.history_table.removeRow(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ProcessorSimulatorApp()
    ex.show()
    sys.exit(app.exec_())