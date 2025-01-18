import os
from pathlib import Path
import zipfile
import py7zr
import lzma
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

class CompressionProfile:
    FAST = "Fast"      # ZIP format, fast compression
    NORMAL = "Normal"  # 7Z format, balanced compression
    MAXIMUM = "Maximum"  # LZMA format, maximum compression

class Compressor:
    def __init__(self):
        self.encryption_key = None
    
    def generate_key(self, password=None):
        if password:
            # Generate a key from the password
            salt = b'zipper_salt'  # In production, use a random salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        else:
            # Generate a random key
            key = Fernet.generate_key()
        
        self.encryption_key = key
        return key
    
    def compress_files(self, files, output_path, profile=CompressionProfile.NORMAL):
        output_path = Path(output_path)
        
        # Create output directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if profile == CompressionProfile.FAST:
            self._compress_zip(files, output_path)
        elif profile == CompressionProfile.NORMAL:
            self._compress_7z(files, output_path)
        else:  # MAXIMUM
            self._compress_lzma(files, output_path)
    
    def _compress_zip(self, files, output_path):
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in files:
                file_path = Path(file)
                zf.write(file_path, file_path.name)
    
    def _compress_7z(self, files, output_path):
        with py7zr.SevenZipFile(output_path, 'w') as sz:
            for file in files:
                file_path = Path(file)
                sz.write(file_path, file_path.name)
    
    def _compress_lzma(self, files, output_path):
        if len(files) == 1:
            # Single file: direct LZMA compression
            with lzma.open(output_path, 'wb') as lz:
                with open(files[0], 'rb') as f:
                    lz.write(f.read())
        else:
            # Multiple files: create ZIP first, then compress with LZMA
            with lzma.open(output_path, 'wb') as lz:
                with zipfile.ZipFile(lz, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for file in files:
                        file_path = Path(file)
                        zf.write(file_path, file_path.name)
    
    def extract_files(self, archive_path, output_dir):
        archive_path = Path(archive_path)
        output_dir = Path(output_dir)
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        ext = archive_path.suffix.lower()
        
        if ext == '.zip':
            self._extract_zip(archive_path, output_dir)
        elif ext == '.7z':
            self._extract_7z(archive_path, output_dir)
        elif ext == '.xz':
            self._extract_lzma(archive_path, output_dir)
        else:
            raise ValueError(f"Unsupported archive format: {ext}")
    
    def _extract_zip(self, archive_path, output_dir):
        with zipfile.ZipFile(archive_path, 'r') as zf:
            zf.extractall(output_dir)
    
    def _extract_7z(self, archive_path, output_dir):
        with py7zr.SevenZipFile(archive_path, 'r') as sz:
            sz.extractall(output_dir)
    
    def _extract_lzma(self, archive_path, output_dir):
        with lzma.open(archive_path, 'rb') as lz:
            try:
                # Try to open as ZIP (multiple files)
                with zipfile.ZipFile(lz) as zf:
                    zf.extractall(output_dir)
            except zipfile.BadZipFile:
                # Not a ZIP, treat as single file
                lz.seek(0)
                output_file = output_dir / archive_path.stem
                with open(output_file, 'wb') as f:
                    f.write(lz.read())
