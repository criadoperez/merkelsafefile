import hashlib

def hash_data(data):
    """Hashes the provided data using SHA-256."""
    hasher = hashlib.sha256()
    if not isinstance(data, bytes):
        data = data.encode('utf-8')  # Ensures that the data is in bytes
    hasher.update(data)
    return hasher.hexdigest()

def hash_file(file_path):
    """Generates a SHA-256 hash for the contents of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()
