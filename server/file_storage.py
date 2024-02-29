import os

class FileStorage:
    def __init__(self, storage_dir="server_files"):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

    def save_file(self, file, filename):
        """Saves an uploaded file to the storage directory."""
        file_path = os.path.join(self.storage_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(file.read())
        return file_path

    def get_file(self, filename):
        """Retrieves a file from the storage directory."""
        file_path = os.path.join(self.storage_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                return f.read()
        return None
