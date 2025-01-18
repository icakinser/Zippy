from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QPushButton,
                            QFileDialog, QComboBox, QSpinBox, QLineEdit,
                            QFormLayout, QDialogButtonBox, QListWidget,
                            QHBoxLayout, QCheckBox, QDateTimeEdit, QTableWidget,
                            QTableWidgetItem, QHeaderView, QCalendarWidget, QTimeEdit,
                            QGroupBox, QMessageBox, QCalendarWidget, QTimeEdit, QScrollArea)
from PyQt6.QtCore import Qt, QDateTime, QSize
from PyQt6.QtGui import QIcon
from ..features.compression import CompressionProfile

class ScheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule Compression")
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        self.datetime_edit = QDateTimeEdit(QDateTime.currentDateTime())
        self.datetime_edit.setCalendarPopup(True)
        form.addRow("Schedule Time:", self.datetime_edit)
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_schedule_time(self):
        return self.datetime_edit.dateTime()

class MonitoredFolderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Monitored Folder")
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Folder selection
        folder_layout = QHBoxLayout()
        self.folder_edit = QLineEdit()
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(browse_btn)
        form.addRow("Folder:", folder_layout)
        
        # File patterns
        self.patterns_edit = QLineEdit()
        self.patterns_edit.setPlaceholderText("*.txt, *.pdf, etc.")
        form.addRow("File Patterns:", self.patterns_edit)
        
        # Minimum file size
        self.min_size = QSpinBox()
        self.min_size.setRange(0, 1000000)
        self.min_size.setSuffix(" KB")
        form.addRow("Minimum File Size:", self.min_size)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_edit.setText(folder)
    
    def get_settings(self):
        return {
            "folder": self.folder_edit.text(),
            "patterns": [p.strip() for p in self.patterns_edit.text().split(",")],
            "min_size": self.min_size.value() * 1024  # Convert KB to bytes
        }

class MonitorSettingsDialog(QDialog):
    def __init__(self, monitors, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Folder Monitor Settings")
        self.monitors = monitors.copy()
        
        layout = QVBoxLayout(self)
        
        # List of monitored folders
        self.list_widget = QListWidget()
        self.update_list()
        layout.addWidget(self.list_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add")
        add_btn.clicked.connect(self.add_monitor)
        button_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_monitor)
        button_layout.addWidget(remove_btn)
        
        layout.addLayout(button_layout)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def update_list(self):
        self.list_widget.clear()
        for monitor in self.monitors:
            self.list_widget.addItem(monitor["folder"])
    
    def add_monitor(self):
        dialog = MonitoredFolderDialog(self)
        if dialog.exec():
            self.monitors.append(dialog.get_settings())
            self.update_list()
    
    def remove_monitor(self):
        current = self.list_widget.currentRow()
        if current >= 0:
            self.monitors.pop(current)
            self.update_list()
    
    def get_monitors(self):
        return self.monitors

class FilePreviewDialog(QDialog):
    def __init__(self, files, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Compression Settings")
        self.files = files
        
        layout = QVBoxLayout(self)
        
        # File list
        layout.addWidget(QLabel("Files to compress:"))
        list_widget = QListWidget()
        for file in files:
            list_widget.addItem(file)
        layout.addWidget(list_widget)
        
        # Compression profile
        form = QFormLayout()
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(["Fast", "Normal", "Maximum"])
        form.addRow("Compression Profile:", self.profile_combo)
        layout.addLayout(form)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def get_settings(self):
        return {
            "profile": self.profile_combo.currentText()
        }

class BatchProcessDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Batch Processing")
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Source directory
        dir_layout = QHBoxLayout()
        self.dir_edit = QLineEdit()
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_directory)
        dir_layout.addWidget(self.dir_edit)
        dir_layout.addWidget(browse_btn)
        form.addRow("Source Directory:", dir_layout)
        
        # File filters
        self.filters_edit = QLineEdit()
        self.filters_edit.setPlaceholderText("*.txt, *.pdf, etc.")
        form.addRow("File Filters:", self.filters_edit)
        
        # Schedule option
        self.schedule_check = QCheckBox("Schedule for later")
        form.addRow("", self.schedule_check)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.dir_edit.setText(directory)
    
    def get_settings(self):
        return {
            "source_dir": self.dir_edit.text(),
            "filters": [f.strip() for f in self.filters_edit.text().split(",") if f.strip()],
            "schedule": self.schedule_check.isChecked()
        }

class EncryptionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set Encryption Password")
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Password fields
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Password:", self.password_edit)
        
        self.confirm_edit = QLineEdit()
        self.confirm_edit.setEchoMode(QLineEdit.EchoMode.Password)
        form.addRow("Confirm Password:", self.confirm_edit)
        
        layout.addLayout(form)
        
        # Warning label
        warning = QLabel("Warning: Keep this password safe. If you lose it, "
                      "you won't be able to decrypt your files!")
        warning.setWordWrap(True)
        warning.setStyleSheet("color: red;")
        layout.addWidget(warning)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def validate(self):
        if self.password_edit.text() != self.confirm_edit.text():
            QMessageBox.warning(self, "Error", "Passwords do not match!")
            return
        if len(self.password_edit.text()) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters!")
            return
        self.accept()
    
    def get_password(self):
        return self.password_edit.text()

class ExtractDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Extract Archive")
        layout = QVBoxLayout(self)
        
        form = QFormLayout()
        
        # Archive file selection
        archive_layout = QHBoxLayout()
        self.archive_edit = QLineEdit()
        archive_btn = QPushButton("Browse...")
        archive_btn.clicked.connect(self.browse_archive)
        archive_layout.addWidget(self.archive_edit)
        archive_layout.addWidget(archive_btn)
        form.addRow("Archive:", archive_layout)
        
        # Output directory selection
        output_layout = QHBoxLayout()
        self.output_edit = QLineEdit()
        output_btn = QPushButton("Browse...")
        output_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(output_btn)
        form.addRow("Extract to:", output_layout)
        
        layout.addLayout(form)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
    
    def browse_archive(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Archive",
            "",
            "Archives (*.zip *.7z *.xz)"
        )
        if file:
            self.archive_edit.setText(file)
    
    def browse_output(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_edit.setText(directory)
    
    def get_paths(self):
        return self.archive_edit.text(), self.output_edit.text()

class OldScheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Schedule Compression")
        self.setMinimumSize(400, 500)
        
        layout = QVBoxLayout()
        
        # Date selection
        date_group = QGroupBox("Date")
        date_layout = QVBoxLayout()
        self.calendar = QCalendarWidget()
        date_layout.addWidget(self.calendar)
        date_group.setLayout(date_layout)
        layout.addWidget(date_group)
        
        # Time selection
        time_group = QGroupBox("Time")
        time_layout = QVBoxLayout()
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        time_layout.addWidget(self.time_edit)
        time_group.setLayout(time_layout)
        layout.addWidget(time_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Schedule")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_schedule_time(self):
        date = self.calendar.selectedDate()
        time = self.time_edit.time()
        return QDateTime(date, time)

class OldMonitoredFolderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Monitored Folder")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        # Folder selection
        folder_group = QGroupBox("Folder Selection")
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("No folder selected")
        select_btn = QPushButton("Select Folder")
        select_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(select_btn)
        folder_group.setLayout(folder_layout)
        layout.addWidget(folder_group)
        
        # File patterns
        patterns_group = QGroupBox("File Patterns")
        patterns_layout = QVBoxLayout()
        patterns_layout.addWidget(QLabel("Enter file patterns to monitor (comma separated):"))
        self.patterns_edit = QLineEdit()
        self.patterns_edit.setPlaceholderText("*.txt, *.docx, *.pdf")
        patterns_layout.addWidget(self.patterns_edit)
        patterns_group.setLayout(patterns_layout)
        layout.addWidget(patterns_group)
        
        # Compression settings
        compress_group = QGroupBox("Compression Settings")
        compress_layout = QVBoxLayout()
        
        # Profile selection
        profile_layout = QHBoxLayout()
        profile_layout.addWidget(QLabel("Compression Profile:"))
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(CompressionProfile.get_default_profiles().keys())
        profile_layout.addWidget(self.profile_combo)
        compress_layout.addLayout(profile_layout)
        
        # Minimum file size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Minimum File Size (KB):"))
        self.size_spin = QSpinBox()
        self.size_spin.setRange(0, 1000000)
        self.size_spin.setValue(100)
        size_layout.addWidget(self.size_spin)
        compress_layout.addLayout(size_layout)
        
        # Auto-delete option
        self.delete_check = QCheckBox("Delete original files after compression")
        compress_layout.addWidget(self.delete_check)
        
        compress_group.setLayout(compress_layout)
        layout.addWidget(compress_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Add Monitor")
        ok_button.clicked.connect(self.validate_and_accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.folder_path = None
    
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder to Monitor"
        )
        if folder:
            self.folder_path = folder
            self.folder_label.setText(folder)
    
    def validate_and_accept(self):
        if not self.folder_path:
            QMessageBox.warning(self, "Error", "Please select a folder to monitor!")
            return
        if not self.patterns_edit.text().strip():
            QMessageBox.warning(self, "Error", "Please enter at least one file pattern!")
            return
        self.accept()
    
    def get_settings(self):
        return {
            "folder": self.folder_path,
            "patterns": [p.strip() for p in self.patterns_edit.text().split(",") if p.strip()],
            "profile": self.profile_combo.currentText(),
            "min_size": self.size_spin.value() * 1024,  # Convert KB to bytes
            "auto_delete": self.delete_check.isChecked()
        }

class OldMonitorSettingsDialog(QDialog):
    def __init__(self, monitors, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Folder Monitors")
        self.setMinimumSize(800, 500)
        
        layout = QVBoxLayout()
        
        # Monitors table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Folder", "Patterns", "Profile", "Min Size", "Auto-Delete"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
        # Add monitors to table
        self.update_table(monitors)
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_button = QPushButton("Add Monitor")
        add_button.clicked.connect(self.add_monitor)
        button_layout.addWidget(add_button)
        
        remove_button = QPushButton("Remove Selected")
        remove_button.clicked.connect(self.remove_monitor)
        button_layout.addWidget(remove_button)
        
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.monitors = monitors.copy()
    
    def update_table(self, monitors):
        self.table.setRowCount(len(monitors))
        for i, monitor in enumerate(monitors):
            self.table.setItem(i, 0, QTableWidgetItem(monitor["folder"]))
            self.table.setItem(i, 1, QTableWidgetItem(", ".join(monitor["patterns"])))
            self.table.setItem(i, 2, QTableWidgetItem(monitor["profile"]))
            self.table.setItem(i, 3, QTableWidgetItem(f"{monitor['min_size'] // 1024} KB"))
            self.table.setItem(i, 4, QTableWidgetItem("Yes" if monitor["auto_delete"] else "No"))
    
    def add_monitor(self):
        dialog = OldMonitoredFolderDialog(self)
        if dialog.exec():
            settings = dialog.get_settings()
            self.monitors.append(settings)
            self.update_table(self.monitors)
    
    def remove_monitor(self):
        selected_rows = set(item.row() for item in self.table.selectedItems())
        if not selected_rows:
            return
        
        # Remove from bottom to top to avoid index shifting
        for row in sorted(selected_rows, reverse=True):
            self.monitors.pop(row)
        
        self.update_table(self.monitors)
    
    def get_monitors(self):
        return self.monitors

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Zipper Help")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Create scrollable text label
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        content = QLabel()
        content.setWordWrap(True)
        content.setTextFormat(Qt.TextFormat.PlainText)
        content.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        
        # Load help content
        try:
            import os
            help_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
                                   "docs", "user_guide.md")
            with open(help_file, "r") as f:
                content.setText(f.read())
        except Exception as e:
            content.setText(f"Error loading help content: {str(e)}\n\nPlease check the documentation at our website.")
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        # Add close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        # Set dialog style
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                padding: 20px;
                background-color: white;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
                font-size: 14px;
                line-height: 1.6;
            }
            QPushButton {
                padding: 6px 12px;
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
