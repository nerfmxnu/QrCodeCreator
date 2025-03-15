import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import qrcode
from PIL import Image
import io

class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator")
        self.setFixedSize(300, 400)
        self.setStyleSheet("""
            QWidget {
                background-color: #2C2C2C;
                font-family: Arial;
                font-size: 12px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
            QLabel {
                color: #E0E0E0;
            }
            QLineEdit {
                background-color: #3C3C3C;
                color: #E0E0E0;
                border: 1px solid #555555;
                padding: 5px;
            }
        """)
        self.qr_image = None

        self.instruction_label = QLabel("Enter text or link:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter text or link here")
        self.generate_button = QPushButton("Generate QR Code")
        self.qr_label = QLabel()
        self.qr_label.setAlignment(Qt.AlignCenter)
        self.save_button = QPushButton("Save QR Code")
        self.save_button.setEnabled(False)
        self.status_label = QLabel()

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.instruction_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.qr_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.save_button)
        layout.addWidget(self.status_label)
        layout.addStretch(1)
        self.setLayout(layout)

        self.generate_button.clicked.connect(self.generate_qr)
        self.save_button.clicked.connect(self.save_qr)

    def generate_qr(self):
        text = self.input_field.text()
        if not text:
            self.status_label.setText("Please enter some text.")
            return
        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(text)
            qr.make(fit=True)
            self.qr_image = qr.make_image(fill_color="black", back_color="white")
            display_img = self.qr_image.resize((200, 200), Image.LANCZOS)
            byte_arr = io.BytesIO()
            display_img.save(byte_arr, format='PNG')
            qimg = QImage.fromData(byte_arr.getvalue())
            pixmap = QPixmap.fromImage(qimg)
            self.qr_label.setPixmap(pixmap)
            self.save_button.setEnabled(True)
            self.status_label.setText("QR code generated.")
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

    def save_qr(self):
        if self.qr_image is None:
            self.status_label.setText("No QR code to save.")
            return
        file_name, _ = QFileDialog.getSaveFileName(self, "Save QR Code", "", "PNG Files (*.png)")
        if file_name:
            try:
                self.qr_image.save(file_name)
                self.status_label.setText("Saved successfully.")
            except Exception as e:
                self.status_label.setText(f"Error saving file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeGenerator()
    window.show()
    sys.exit(app.exec_())
