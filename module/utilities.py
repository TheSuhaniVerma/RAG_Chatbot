import os
import shutil


def clear_temp_folder(folder="temp_files"):
    """Remove temporary or stored folders."""
    if os.path.exists(folder):
        shutil.rmtree(folder)
