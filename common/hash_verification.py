import os
import sys
import hashlib


# Adjust the path below to the directory containing your 'client.py' and 'hash_utils.py' modules
# sys.path.append('/path/to/your/modules')

# Import the necessary modules
# import client
# import hash_utils

from client import hash_file as client_hash_file
from hash_utils import hash_file as hash_utils_hash_file

# Your existing code to check the current working directory
print("Current Working Directory: ", os.getcwd())

file_path = '/home/alejandro/parischallenge/file1.txt'
# Verify and align hashing methods across client and server

# Ensure hash_file functions in client.py and hash_utils.py are consistent
assert client_hash_file(file_path) == hash_utils_hash_file(file_path), "Hashing functions are inconsistent"
print(client_hash_file(file_path))
print(hash_utils_hash_file(file_path))


# Ensure file data is not altered during upload in client.py and server.py
# This step involves checking how files are read, uploaded, and stored
# Example check (pseudo-code):
# assert client.upload_file(file) == server.receive_file(file), "File data altered during upload"

# Verify Merkle tree construction in merkle.py
# Ensure leaf nodes are correctly created from file hashes and parent nodes correctly combine child hashes
# Example check (pseudo-code):
# assert merkle_tree.root.hash == expected_root_hash, "Merkle tree construction is incorrect"

# Confirm file hash re-computation on the server matches the initial hash
# This involves re-hashing the file upon request in server.py and comparing it to the initial hash
# Example check (pseudo-code):
# assert server.recompute_file_hash(file) == initial_file_hash, "File hash verification failed"
