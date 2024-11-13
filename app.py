import sys
import os
import sqlite3
import pandas as pd
import pdfkit
import markdown2
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox, QFileDialog, QLineEdit, QCheckBox, QGroupBox, QHBoxLayout, QProgressBar, QComboBox
)
from PyQt6.QtCore import (Qt,QTimer)
from PIL import Image
import platform

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

# Register window
class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.resize(350, 250)

        # Input Group
        input_group = QGroupBox("Create a New Account")
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Layout for input fields
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.username_label)
        input_layout.addWidget(self.username_input)
        input_layout.addWidget(self.password_label)
        input_layout.addWidget(self.password_input)
        input_layout.addWidget(self.show_password_checkbox)
        input_group.setLayout(input_layout)

        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(input_group)
        main_layout.addWidget(self.register_button)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)
    
    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Both fields are required.")
            return

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            QMessageBox.information(self, "Success", "Registration successful!")
            self.clear_inputs()
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Username already exists.")
        finally:
            conn.close()
    
    def clear_inputs(self):
        self.username_input.clear()
        self.password_input.clear()
        self.show_password_checkbox.setChecked(False)

def open_file(pdf_path, event=None):
    if platform.system() == "Windows":
        os.startfile(pdf_path)
    elif platform.system() == "Darwin":  # macOS
        os.system(f'open "{pdf_path}"')
    elif platform.system() == "Linux":
        os.system(f'xdg-open "{pdf_path}"')

# Menu window with file conversion functionality
class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Conversion to PDF or DOCX")
        self.resize(500, 300)

        # File selection group
        file_selection_group = QGroupBox("File Selection")
        self.supported_files_label = QLabel("Supported file types: DOCX, CSV, TXT, XLSX, PNG, JPG, JPEG, HTML, MD")
        self.file_label = QLabel("No file selected.")
        self.select_button = QPushButton("Select File")
        self.select_button.clicked.connect(self.select_file)

        file_selection_layout = QVBoxLayout()
        file_selection_layout.addWidget(self.supported_files_label)
        file_selection_layout.addWidget(self.file_label)
        file_selection_layout.addWidget(self.select_button)
        file_selection_group.setLayout(file_selection_layout)

        # Conversion format selection
        self.format_combo = QComboBox()
        self.format_combo.addItem("Convert to PDF")
        self.format_combo.addItem("Convert to DOCX")

        # Conversion and logout group
        action_group = QGroupBox("Actions")
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.start_conversion)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)

        action_layout = QHBoxLayout()
        action_layout.addWidget(self.format_combo)
        action_layout.addWidget(self.convert_button)
        action_layout.addWidget(self.logout_button)
        action_group.setLayout(action_layout)

        # Progress bar for conversion
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(file_selection_group)
        main_layout.addWidget(action_group)
        main_layout.addWidget(self.progress_bar)
        
        self.setLayout(main_layout)
        self.file_path = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Select File", "", "Files (*.docx *.csv *.txt *.xlsx *.png *.jpg *.jpeg *.html *.md)"
        )
        if file_path:
            self.file_path = file_path
            self.file_label.setText(f"Selected: {file_path}")
            self.progress_bar.setValue(0)

    def start_conversion(self):
        if not self.file_path:
            QMessageBox.warning(self, "Warning", "Please select a file first.")
            return
        
        self.progress_bar.setValue(0)
        self.timer.start(100)  # Start timer for progress simulation

    def update_progress(self):
        # Simulate progress
        value = self.progress_bar.value()
        if value < 100:
            self.progress_bar.setValue(value + 10)
        else:
            self.timer.stop()
            # Check selected format and call the appropriate conversion function
            if self.format_combo.currentText() == "Convert to PDF":
                self.convert_to_pdf()
            elif self.format_combo.currentText() == "Convert to DOCX":
                self.convert_to_docx()

    def convert_to_pdf(self):
        try:
            if self.file_path.endswith('.docx'):
                self.convert_docx_to_pdf(self.file_path)
            elif self.file_path.endswith('.csv'):
                self.convert_csv_to_pdf(self.file_path)
            elif self.file_path.endswith('.txt'):
                self.convert_txt_to_pdf(self.file_path)
            elif self.file_path.endswith('.xlsx'):
                self.convert_excel_to_pdf(self.file_path)
            elif self.file_path.endswith(('.png', '.jpg', '.jpeg')):
                self.convert_image_to_pdf(self.file_path)
            elif self.file_path.endswith('.html'):
                self.convert_html_to_pdf(self.file_path)
            elif self.file_path.endswith('.md'):
                self.convert_markdown_to_pdf(self.file_path)
            else:
                QMessageBox.warning(self, "Warning", "Unsupported file type.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert file to PDF: {e}")

    def convert_to_docx(self):
        # Example of converting other formats to DOCX
        try:
            docx_path = self.file_path.rsplit('.', 1)[0] + '.docx'
            if self.file_path.endswith('.txt'):
                doc = Document()
                with open(self.file_path, "r") as file:
                    for line in file:
                        doc.add_paragraph(line.strip())
                doc.save(docx_path)
            # Implement additional conversions to DOCX as needed
            QMessageBox.information(self, "Success", f"File converted to DOCX: {docx_path}")
            open_file(docx_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to convert file to DOCX: {e}")

    def convert_docx_to_pdf(self, file_path):
        doc = Document(file_path)
        pdf_path = file_path.replace('.docx', '.pdf')
        c = canvas.Canvas(pdf_path, pagesize=letter)
        text_object = c.beginText(50, 750)
        for para in doc.paragraphs:
            text_object.textLine(para.text)
        c.drawText(text_object)
        c.save()
        QMessageBox.information(self, "Success", f"DOCX converted to PDF: {pdf_path}")
        open_file(pdf_path)

    def convert_csv_to_pdf(self, file_path):
        df = pd.read_csv(file_path)
        pdf_path = file_path.replace('.csv', '.pdf')
        c = canvas.Canvas(pdf_path, pagesize=letter)
        text_object = c.beginText(50, 750)
        text_object.textLine(" | ".join(df.columns))
        text_object.textLine("-" * 50)
        for _, row in df.iterrows():
            text_object.textLine(" | ".join(str(value) for value in row))
        c.drawText(text_object)
        c.save()
        QMessageBox.information(self, "Success", f"CSV converted to PDF: {pdf_path}")
        open_file(pdf_path)

    def convert_txt_to_pdf(self, file_path):
        pdf_path = file_path.replace('.txt', '.pdf')
        c = canvas.Canvas(pdf_path, pagesize=letter)
        with open(file_path, "r") as file:
            text = file.read()
            text_object = c.beginText(50, 750)
            text_object.setFont("Helvetica", 12)
            text_object.textLines(text)
            c.drawText(text_object)
        c.save()
        QMessageBox.information(self, "Success", f"TXT converted to PDF: {pdf_path}")
        open_file(pdf_path)

    def convert_excel_to_pdf(self, file_path):
        df = pd.read_excel(file_path)
        pdf_path = file_path.replace('.xlsx', '.pdf')
        df.to_html("temp.html")
        pdfkit.from_file("temp.html", pdf_path)
        QMessageBox.information(self, "Success", f"Excel converted to PDF: {pdf_path}")
        open_file(pdf_path)

    def convert_image_to_pdf(self, file_path):
        image = Image.open(file_path)
        pdf_path = file_path.rsplit('.', 1)[0] + '.pdf'
        image.convert('RGB').save(pdf_path, "PDF")
        QMessageBox.information(self, "Success", f"Image converted to PDF: {pdf_path}")
        open_file(pdf_path)

    def convert_html_to_pdf(self, file_path):
        pdf_path = file_path.replace('.html', '.pdf')
        pdfkit.from_file(file_path, pdf_path)
        QMessageBox.information(self, "Success", f"HTML converted to PDF: {pdf_path}")
        open_file(pdf_path)

    def convert_markdown_to_pdf(self, file_path):
        with open(file_path, "r") as file:
            html = markdown2.markdown(file.read())
            with open("temp.html", "w") as temp_file:
                temp_file.write(html)
        pdf_path = file_path.replace('.md', '.pdf')
        pdfkit.from_file("temp.html", pdf_path)
        QMessageBox.information(self, "Success", f"Markdown converted to PDF: {pdf_path}")
        open_file(pdf_path)

    def logout(self):
        self.close()
        login_window.show()  # Show the login window again after logout

# Login window
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(350, 250)

        # Group box for login form
        login_group = QGroupBox("Login to Your Account")
        
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Layout for input fields
        login_layout = QVBoxLayout()
        login_layout.addWidget(self.username_label)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.password_label)
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(self.show_password_checkbox)
        login_group.setLayout(login_layout)

        # Buttons for login and register
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_user)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.open_register_window)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(login_group)
        main_layout.addLayout(button_layout)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)
    
    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
    
    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            QMessageBox.information(self, "Success", "Login successful!")
            self.clear_inputs()
            self.open_menu_window()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")
    
    def clear_inputs(self):
        self.username_input.clear()
        self.password_input.clear()
        self.show_password_checkbox.setChecked(False)
    
    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()
    
    def open_menu_window(self):
        self.menu_window = MenuWindow()
        self.menu_window.show()

# Main application
app = QApplication(sys.argv)
init_db()  # Initialize the database

login_window = LoginWindow()
login_window.show()

sys.exit(app.exec())
