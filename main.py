import json
import re
import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QFileDialog, QGridLayout, QMessageBox, QTextEdit
)
from PyQt5.QtCore import QThread, pyqtSignal
from config import system_prompt_image_to_json, system_prompt_text_to_json
from processing.formatter import format_elapsed, process_image_to_json, process_text_to_json

class Worker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(str)

    def __init__(self, mode, images_folder, texts_folder, output_file, log_file):
        super().__init__()
        self.mode = mode
        self.images_folder = images_folder
        self.texts_folder = texts_folder
        self.output_file = output_file
        self.log_file = log_file

    def run(self):
        start_time = time.time()
        try:
            if self.mode == "image":
                files = [f for f in os.listdir(self.images_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                for i, filename in enumerate(files, 1):
                    file_path = os.path.join(self.images_folder, filename)
                    self.progress.emit(f"START: Processing image {i}/{len(files)}: {filename}")
                    file_start = time.time()
                    status, elapsed = self.process_image_with_status(file_path)
                    self.progress.emit(f"{status} ({elapsed:.2f}s)\n")
            elif self.mode == "text":
                files = [f for f in os.listdir(self.texts_folder) if f.lower().endswith('.txt')]
                for i, filename in enumerate(files, 1):
                    file_path = os.path.join(self.texts_folder, filename)
                    file_start = time.time()
                    status, elapsed = self.process_text_with_status(file_path)
                    self.progress.emit(f"{os.path.basename(file_path)}: {status} ({format_elapsed(elapsed)})\n")
            else:
                self.finished.emit("Invalid MODE selected. Use 'image' or 'text'.")
                return
            end_time = time.time()
            total_time = end_time - start_time
            minutes = int(total_time // 60)
            seconds = int(total_time % 60)
            self.finished.emit(f"Processing complete!\nTime: {minutes}m {seconds}s")
        except Exception as e:
            self.finished.emit(f"Error: {str(e)}")

    def process_image_with_status(self, image_path):
        from processing.formatter import process_image_to_json
        file_start = time.time()
        try:
            self.progress.emit("START: Extracting text from image...")
            status = process_image_to_json(
                image_path, self.output_file, system_prompt_image_to_json, self.log_file, self.progress
            )
            elapsed = time.time() - file_start
            return (f"{os.path.basename(image_path)}: {status}", elapsed)
        except Exception as e:
            elapsed = time.time() - file_start
            return (f"{os.path.basename(image_path)}: Failed ({str(e)})", elapsed)

    def process_text_with_status(self, text_path):
        from processing.formatter import process_text_to_json
        file_start = time.time()
        try:
            status = process_text_to_json(
                text_path, self.output_file, system_prompt_text_to_json, self.log_file, self.progress
            )
            elapsed = time.time() - file_start
            return (f"{os.path.basename(text_path)}: {status}", elapsed)
        except Exception as e:
            elapsed = time.time() - file_start
            return (f"{os.path.basename(text_path)}: Failed ({str(e)})", elapsed)

class QuizProcessorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Quiz Processor")
        self.setFixedSize(600, 480)
        layout = QGridLayout()

        # Mode
        layout.addWidget(QLabel("Mode:"), 0, 0)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["text", "image"])
        layout.addWidget(self.mode_combo, 0, 1, 1, 2)

        # Images Folder
        layout.addWidget(QLabel("Images Folder:"), 1, 0)
        self.images_folder_edit = QLineEdit("data/images")
        layout.addWidget(self.images_folder_edit, 1, 1)
        btn_img = QPushButton("Browse")
        btn_img.clicked.connect(lambda: self.browse_folder(self.images_folder_edit))
        layout.addWidget(btn_img, 1, 2)

        # Texts Folder
        layout.addWidget(QLabel("Texts Folder:"), 2, 0)
        self.texts_folder_edit = QLineEdit("data/texts")
        layout.addWidget(self.texts_folder_edit, 2, 1)
        btn_txt = QPushButton("Browse")
        btn_txt.clicked.connect(lambda: self.browse_folder(self.texts_folder_edit))
        layout.addWidget(btn_txt, 2, 2)

        # Output File
        layout.addWidget(QLabel("Output File:"), 3, 0)
        self.output_file_edit = QLineEdit("output/formatted_questions.json")
        layout.addWidget(self.output_file_edit, 3, 1)
        btn_out = QPushButton("Browse")
        btn_out.clicked.connect(lambda: self.browse_file(self.output_file_edit))
        layout.addWidget(btn_out, 3, 2)

        # Log File
        layout.addWidget(QLabel("Log File:"), 4, 0)
        self.log_file_edit = QLineEdit("output/deep_think_logs.txt")
        layout.addWidget(self.log_file_edit, 4, 1)
        btn_log = QPushButton("Browse")
        btn_log.clicked.connect(lambda: self.browse_file(self.log_file_edit))
        layout.addWidget(btn_log, 4, 2)

        # Log Window
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        layout.addWidget(self.log_window, 5, 0, 1, 3)

        # Run Button
        self.run_btn = QPushButton("Run")
        self.run_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; height: 32px;")
        self.run_btn.clicked.connect(self.run_processing)
        layout.addWidget(self.run_btn, 6, 0, 1, 3)

        # Remove Prefixes Section
        layout.addWidget(QLabel("Remove prefixes from JSON:"), 7, 0)
        self.prefix_input_edit = QLineEdit()
        layout.addWidget(self.prefix_input_edit, 7, 1)
        btn_prefix = QPushButton("Browse")
        btn_prefix.clicked.connect(lambda: self.browse_file(self.prefix_input_edit))
        layout.addWidget(btn_prefix, 7, 2)

        self.prefix_btn = QPushButton("Remove Prefixes")
        self.prefix_btn.setStyleSheet("background-color: #1976D2; color: white; font-weight: bold; height: 32px;")
        self.prefix_btn.clicked.connect(self.remove_prefixes_from_json)
        layout.addWidget(self.prefix_btn, 8, 0, 1, 3)

        self.setLayout(layout)
        self.worker = None

    def browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            line_edit.setText(folder)

    def browse_file(self, line_edit):
        file, _ = QFileDialog.getSaveFileName(self, "Select File", "", "JSON Files (*.json);;All Files (*)")
        if file:
            line_edit.setText(file)

    def run_processing(self):
        mode = self.mode_combo.currentText()
        images_folder = self.images_folder_edit.text()
        texts_folder = self.texts_folder_edit.text()
        output_file = self.output_file_edit.text()
        log_file = self.log_file_edit.text()

        self.log_window.clear()
        self.run_btn.setEnabled(False)
        self.run_btn.setText("Processing...")
        self.run_btn.setStyleSheet("background-color: #bdbdbd; color: #888; font-weight: bold; height: 32px;")

        self.worker = Worker(mode, images_folder, texts_folder, output_file, log_file)
        self.worker.progress.connect(self.append_log)
        self.worker.finished.connect(self.processing_finished)
        self.worker.start()

    def append_log(self, message):
        self.log_window.append(message)

    def processing_finished(self, message):
        self.run_btn.setEnabled(True)
        self.run_btn.setText("Run")
        self.run_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; height: 32px;")
        self.log_window.append(message)
        if message.startswith("Error"):
            QMessageBox.critical(self, "Error", message)
        else:
            QMessageBox.information(self, "Done", message)

    def remove_prefixes_from_json(self):
        # Implement the logic to remove prefixes from JSON keys
        prefix_file = self.prefix_input_edit.text()
        if not os.path.isfile(prefix_file):
            QMessageBox.critical(self, "Error", "Invalid prefix file.")
            return
        try:
            with open(prefix_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            for question in data:
                for answer in question.get("answers", []):
                    answer["text"] = re.sub(r"^([a-zA-Z][\)\.]|\d+[\)\.])\s*", "", answer["text"])

            output_path = os.path.join("output", "questions_without_prefix.json")
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            QMessageBox.information(self, "Done", "Prefixes removed successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = QuizProcessorGUI()
    window.show()
    sys.exit(app.exec_())