import os
import zipfile

EXCLUDE_DIRS = {'.git', 'venv', 'node_modules', '.vscode', '.idea', 'logs', '__pycache__'}
EXCLUDE_EXTS = {'.zip', '.tar.gz', '.rar', '.7z', '.log', '.DS_Store', 'Thumbs.db'}

BACKUP_NAME = 'ai-Q-backup.zip'
ROOT_DIR = os.path.abspath('.')

with zipfile.ZipFile(BACKUP_NAME, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
    for foldername, subfolders, filenames in os.walk(ROOT_DIR):
        # Exclude unwanted directories
        rel_folder = os.path.relpath(foldername, ROOT_DIR)
        if any(part in EXCLUDE_DIRS for part in rel_folder.split(os.sep)):
            continue
        for filename in filenames:
            ext = os.path.splitext(filename)[1]
            if filename in EXCLUDE_EXTS or ext in EXCLUDE_EXTS:
                continue
            file_path = os.path.join(foldername, filename)
            arcname = os.path.relpath(file_path, ROOT_DIR)
            backup_zip.write(file_path, arcname)
print(f"Backup complete: {BACKUP_NAME}") 