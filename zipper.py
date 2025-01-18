import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout,
                          QWidget, QPushButton, QMessageBox, QProgressDialog,
                          QFileDialog, QHBoxLayout, QMenuBar, QMenu,
                          QListWidget)
from PyQt6.QtCore import Qt, QSize, QSettings, QDateTime
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QAction

from zipper_app.features.compression import Compressor, CompressionProfile
from zipper_app.features.monitor import FolderMonitor
from zipper_app.ui.theme import ThemeManager
from zipper_app.ui.dialogs import (ScheduleDialog, MonitoredFolderDialog,
                                MonitorSettingsDialog, FilePreviewDialog,
                                BatchProcessDialog, EncryptionDialog,
                                ExtractDialog, HelpDialog)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zipper - Advanced File Compression Tool")
        self.setFixedSize(QSize(600, 500))
        
        # Load settings
        self.settings = QSettings('Codeium', 'Zipper')
        self.recent_files = self.settings.value('recent_files', [])
        self.is_dark_mode = self.settings.value('dark_mode', False, type=bool)
        self.folder_monitors = self.settings.value('folder_monitors', [])
        
        # Initialize compressor and monitors
        self.compressor = Compressor()
        self.active_monitors = []
        self.setup_folder_monitors()
        
        # Initialize encryption key
        self.encryption_key = None
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create and style the drop zone
        self.drop_label = QLabel("Drop files here to compress\nor click to select files")
        self.drop_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.update_drop_zone_style()
        self.drop_label.mousePressEvent = self.open_file_dialog
        layout.addWidget(self.drop_label)
        
        # Add a status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self.status_label)
        
        # Recent files list
        self.recent_list = QListWidget()
        self.recent_list.setMaximumHeight(100)
        self.recent_list.itemDoubleClicked.connect(self.open_recent_file)
        self.update_recent_files_list()
        layout.addWidget(QLabel("Recent Files:"))
        layout.addWidget(self.recent_list)
        
        # Enable drop events
        self.setAcceptDrops(True)
        
        # Initialize file list
        self.files_to_compress = []
        
        # Add buttons
        button_layout = QHBoxLayout()
        
        select_button = QPushButton("Select Files")
        select_button.clicked.connect(self.open_file_dialog)
        button_layout.addWidget(select_button)
        
        extract_button = QPushButton("Extract Archive")
        extract_button.clicked.connect(self.show_extract_dialog)
        button_layout.addWidget(extract_button)
        
        batch_button = QPushButton("Batch Processing")
        batch_button.clicked.connect(self.show_batch_dialog)
        button_layout.addWidget(batch_button)
        
        layout.addLayout(button_layout)
        
        # Apply theme
        if self.is_dark_mode:
            ThemeManager.apply_dark_theme(QApplication.instance())
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open Files...", self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        
        batch_action = QAction("Batch Processing...", self)
        batch_action.triggered.connect(self.show_batch_dialog)
        file_menu.addAction(batch_action)
        
        extract_action = QAction("Extract Archive...", self)
        extract_action.triggered.connect(self.show_extract_dialog)
        file_menu.addAction(extract_action)
        
        file_menu.addSeparator()
        
        clear_recent_action = QAction("Clear Recent Files", self)
        clear_recent_action.triggered.connect(self.clear_recent_files)
        file_menu.addAction(clear_recent_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu
        settings_menu = menubar.addMenu("Settings")
        
        save_settings_action = QAction("Save Current Settings as Default", self)
        save_settings_action.triggered.connect(self.save_settings)
        settings_menu.addAction(save_settings_action)
        
        reset_settings_action = QAction("Reset to Default Settings", self)
        reset_settings_action.triggered.connect(self.reset_settings)
        settings_menu.addAction(reset_settings_action)
        
        settings_menu.addSeparator()
        
        monitors_action = QAction("Folder Monitors...", self)
        monitors_action.triggered.connect(self.show_monitor_settings)
        settings_menu.addAction(monitors_action)
        
        settings_menu.addSeparator()
        
        theme_menu = settings_menu.addMenu("Theme")
        
        dark_mode_action = QAction("Dark Mode", self)
        dark_mode_action.setCheckable(True)
        dark_mode_action.setChecked(self.is_dark_mode)
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        theme_menu.addAction(dark_mode_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("Tools")
        
        encrypt_action = QAction("Set Encryption Password...", self)
        encrypt_action.triggered.connect(self.set_encryption_password)
        tools_menu.addAction(encrypt_action)
        
        schedule_action = QAction("Schedule Compression...", self)
        schedule_action.triggered.connect(self.schedule_compression)
        tools_menu.addAction(schedule_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        help_action = QAction("Documentation", self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)
        
        help_menu.addSeparator()
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def update_drop_zone_style(self):
        base_style = """
            QLabel {
                border: 2px dashed #aaa;
                border-radius: 10px;
                padding: 20px;
                font-size: 16px;
                min-height: 200px;
            }
            
            QLabel:hover {
                border-color: #999;
            }
        """
        if self.is_dark_mode:
            self.drop_label.setStyleSheet(base_style + """
                QLabel {
                    background: #2d2d2d;
                    color: #ffffff;
                }
                QLabel:hover {
                    background: #353535;
                }
            """)
        else:
            self.drop_label.setStyleSheet(base_style + """
                QLabel {
                    background: #f0f0f0;
                    color: black;
                }
                QLabel:hover {
                    background: #e0e0e0;
                }
            """)
    
    def toggle_dark_mode(self, checked):
        self.is_dark_mode = checked
        self.settings.setValue('dark_mode', checked)
        
        if checked:
            ThemeManager.apply_dark_theme(QApplication.instance())
        else:
            ThemeManager.apply_light_theme(QApplication.instance())
        self.update_drop_zone_style()
    
    def set_encryption_password(self):
        dialog = EncryptionDialog(self)
        if dialog.exec():
            password = dialog.get_password()
            self.encryption_key = self.compressor.generate_key()
            QMessageBox.information(self, "Success", "Encryption password set successfully!")
    
    def schedule_compression(self):
        if not self.files_to_compress:
            QMessageBox.warning(self, "Error", "Please select files to compress first!")
            return
        
        dialog = ScheduleDialog(self)
        if dialog.exec():
            schedule_time = dialog.get_schedule_time()
            QMessageBox.information(
                self,
                "Compression Scheduled",
                f"Compression scheduled for {schedule_time.toString('yyyy-MM-dd hh:mm')}"
            )
    
    def show_batch_dialog(self):
        dialog = BatchProcessDialog(self)
        if dialog.exec():
            settings = dialog.get_settings()
            if settings["schedule"]:
                self.schedule_compression()
            else:
                self.process_batch(settings)
    
    def process_batch(self, settings):
        if not settings["source_dir"]:
            return
        
        files = []
        for filter_pattern in settings["filters"] or ["*.*"]:
            files.extend(Path(settings["source_dir"]).glob(filter_pattern))
        
        if not files:
            QMessageBox.warning(self, "No Files Found", "No files match the specified filters!")
            return
        
        self.process_files([str(f) for f in files])
    
    def update_recent_files_list(self):
        self.recent_list.clear()
        for file in self.recent_files:
            self.recent_list.addItem(os.path.basename(file))
    
    def add_to_recent_files(self, file_path):
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:10]  # Keep only 10 most recent
        self.settings.setValue('recent_files', self.recent_files)
        self.update_recent_files_list()
    
    def clear_recent_files(self):
        self.recent_files = []
        self.settings.setValue('recent_files', [])
        self.update_recent_files_list()
    
    def open_recent_file(self, item):
        index = self.recent_list.row(item)
        if index >= 0 and index < len(self.recent_files):
            file_path = self.recent_files[index]
            if os.path.exists(file_path):
                if os.path.isdir(file_path):
                    self.process_batch({"source_dir": file_path, "filters": [], "schedule": False})
                else:
                    self.process_files([file_path])
            else:
                QMessageBox.warning(self, "File Not Found", f"The file {file_path} no longer exists!")
                self.recent_files.pop(index)
                self.settings.setValue('recent_files', self.recent_files)
                self.update_recent_files_list()
    
    def process_files(self, files):
        self.files_to_compress = files
        total_size = sum(os.path.getsize(f) for f in files)
        self.status_label.setText(f"Selected {len(files)} files ({self.format_size(total_size)})")
        
        # Show file preview dialog
        preview_dialog = FilePreviewDialog(files, self)
        
        # Load last used settings
        last_profile = self.settings.value('compression_profile', 'Normal')
        preview_dialog.profile_combo.setCurrentText(last_profile)
        
        if preview_dialog.exec():
            settings = preview_dialog.get_settings()
            self.last_used_settings = settings
            
            if settings['profile'] == "Fast":
                ext = ".zip"
            elif settings['profile'] == "Normal":
                ext = ".7z"
            else:
                ext = ".xz"
            
            # Get save location
            default_name = Path(files[0]).stem + ext
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Compressed File",
                str(Path.home() / default_name),  # Use home directory as default
                f"Compressed Files (*{ext})"
            )
            
            if save_path:
                try:
                    # Show progress dialog
                    progress = QProgressDialog("Compressing files...", "Cancel", 0, len(files), self)
                    progress.setWindowModality(Qt.WindowModality.WindowModal)
                    progress.show()
                    
                    self.compressor.compress_files(files, save_path, settings['profile'])
                    
                    # Add to recent files
                    if save_path not in self.recent_files:
                        self.recent_files.insert(0, save_path)
                        if len(self.recent_files) > 10:
                            self.recent_files.pop()
                        self.settings.setValue('recent_files', self.recent_files)
                        self.update_recent_files_list()
                    
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Files compressed successfully to {save_path}"
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to compress files: {str(e)}"
                    )
                finally:
                    progress.close()
    
    @staticmethod
    def format_size(size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    
    def open_file_dialog(self, event=None):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Files to Compress",
            "",
            "All Files (*.*)"
        )
        if files:
            self.process_files(files)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.drop_label.setStyleSheet("""
                QLabel {
                    border: 2px dashed #4CAF50;
                    border-radius: 10px;
                    padding: 20px;
                    background: #E8F5E9;
                    font-size: 16px;
                    min-height: 200px;
                    color: black;
                }
            """)
    
    def dragLeaveEvent(self, event):
        self.update_drop_zone_style()
    
    def dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.process_files(files)
        self.update_drop_zone_style()
    
    def show_extract_dialog(self):
        dialog = ExtractDialog(self)
        if dialog.exec():
            archive_path, output_dir = dialog.get_paths()
            if archive_path and output_dir:
                try:
                    # Show progress dialog
                    progress = QProgressDialog("Extracting files...", "Cancel", 0, 100, self)
                    progress.setWindowModality(Qt.WindowModality.WindowModal)
                    progress.show()
                    
                    # Extract files
                    self.compressor.extract_files(archive_path, output_dir)
                    
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Files extracted successfully to {output_dir}"
                    )
                except Exception as e:
                    QMessageBox.critical(
                        self,
                        "Error",
                        f"Failed to extract files: {str(e)}"
                    )
                finally:
                    progress.close()
    
    def show_about(self):
        QMessageBox.about(
            self,
            "About Zipper",
            "Zipper - Advanced File Compression Tool\n\n"
            "A modern, feature-rich file compression utility with support for "
            "multiple formats, encryption, and folder monitoring."
        )
    
    def setup_folder_monitors(self):
        # Stop existing monitors
        for monitor in self.active_monitors:
            monitor.stop()
        self.active_monitors.clear()
        
        # Create new monitors
        for monitor_settings in self.folder_monitors:
            monitor = FolderMonitor(
                monitor_settings["folder"],
                monitor_settings["patterns"],
                monitor_settings["min_size"]
            )
            monitor.file_found.connect(
                lambda f, s=monitor_settings: self.handle_monitored_file(f, s)
            )
            monitor.start()
            self.active_monitors.append(monitor)
    
    def show_monitor_settings(self):
        dialog = MonitorSettingsDialog(self.folder_monitors, self)
        if dialog.exec():
            self.folder_monitors = dialog.get_monitors()
            self.settings.setValue('folder_monitors', self.folder_monitors)
            self.setup_folder_monitors()
    
    def handle_monitored_file(self, file_path, settings):
        # Create output path
        output_dir = os.path.join(os.path.dirname(file_path), "compressed")
        os.makedirs(output_dir, exist_ok=True)
        
        base_name = os.path.basename(file_path)
        if settings["profile"] == "Fast":
            ext = ".zip"
        elif settings["profile"] == "Normal":
            ext = ".7z"
        else:
            ext = ".xz"
        
        output_path = os.path.join(output_dir, os.path.splitext(base_name)[0] + ext)
        
        # Start compression
        self.process_files(
            [file_path],
            output_path=output_path,
            profile=settings["profile"],
            auto_delete=settings["auto_delete"]
        )
    
    def closeEvent(self, event):
        # Stop all monitors before closing
        for monitor in self.active_monitors:
            monitor.stop()
        super().closeEvent(event)
    
    def save_settings(self):
        self.settings.setValue('dark_mode', self.is_dark_mode)
        QMessageBox.information(self, "Settings Saved", "Current settings have been saved as default.")
    
    def reset_settings(self):
        self.settings.clear()
        self.is_dark_mode = False
        if self.is_dark_mode:
            ThemeManager.apply_dark_theme(QApplication.instance())
        else:
            ThemeManager.apply_light_theme(QApplication.instance())
        self.update_drop_zone_style()
        QMessageBox.information(self, "Settings Reset", "Settings have been reset to default values.")

    def show_help(self):
        dialog = HelpDialog(self)
        dialog.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for a modern look
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
