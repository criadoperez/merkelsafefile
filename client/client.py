import argparse
import sys
import os
import hashlib  # Make sure to import hashlib for hash_file function
import requests  # Assuming the use of the requests library for HTTP calls

# Modify the system path to include the parent directory, allowing imports from the 'common' directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

 # Import Merkle Tree and hash_data function from the 'common' module
from common.merkle import MerkleTree, hash_data

SERVER_URL = "http://127.0.0.1:5000/upload"
SERVER_REQUEST_URL = "http://127.0.0.1:5000/request_file"

def hash_file(filepath):
    """Reads a file and returns its SHA-256 hash."""
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        content = f.read()
        hasher.update(content)
    return hasher.hexdigest()

def upload_files(filepaths):
    """Uploads a list of files to the server."""
    file_hashes = [hash_file(fp) for fp in filepaths]
    merkle_tree = MerkleTree(file_hashes)
    root_hash = merkle_tree.root.hash

    # Iterate over each file path for upload
    for filepath in filepaths:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(SERVER_URL, files=files)
            if response.status_code == 200:
                print(f"Uploaded {filepath} successfully.")
            else:
                print(f"Failed to upload {filepath}.")

    # Store the root hash of the Merkle Tree locally for later verification
    with open("root_hash.txt", 'w') as f:
        f.write(root_hash)

    # Delete local copies of uploadedfiles
    for filepath in filepaths:
        os.remove(filepath)
        print(f"Deleted {filepath} from local storage.")


    print("Files uploaded and local copies deleted. Root hash stored for verification.")

def verify_file(filename):
    """Requests file and its Merkle proof from the server and verifies file integrity."""
    # Request the file and its Merkle proof from the server
    print(f"Requesting file and proof from the server for {filename}")
    response = requests.get(SERVER_REQUEST_URL, params={'filename': filename})
    if response.status_code == 200:
        data = response.json()
        file_data = data['file_data'].encode('utf-8')  # Assuming file_data is returned as a string
        file_hash = data['file_hash']
        proof = data['proof']

        if not proof:
            print("Received an empty proof. Verification cannot proceed.")
            return

        # Save the file locally under its original name
        with open(filename, 'wb') as f:
            f.write(file_data)
        print(f"File {filename} has been downloaded successfully.")

        # Load the stored root hash
        with open("root_hash.txt", 'r') as f:
            root_hash = f.read()

        # Debugging output for verification process
        print(f"File hash: {file_hash}")
        print(f"Proof: {proof}")
        print(f"Stored root hash: {root_hash}")

        # Verify the proof
        merkle_tree = MerkleTree([])  # Initialize an empty Merkle tree for proof verification
        is_valid = merkle_tree.verify_proof(file_hash, proof, root_hash)

        if is_valid:
            print(f"The file {filename} is verified and intact.")
        else:
            print(f"The file {filename} could not be verified.")
    else:
        print("Failed to request the file from the server.")


def main():
    parser = argparse.ArgumentParser(description="Client for file upload and verification")
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for upload command
    upload_parser = subparsers.add_parser('upload', help='Upload files')
    upload_parser.add_argument('filepaths', nargs='+', help='Paths of files to upload')

    # Subparser for verify command
    verify_parser = subparsers.add_parser('verify', help='Verify file integrity')
    verify_parser.add_argument('filename', help='Name of the file to verify')

    args = parser.parse_args()

    # Execute the appropriate function based on the command line arguments
    if args.command == 'upload':
        upload_files(args.filepaths)
    elif args.command == 'verify':
        verify_file(args.filename)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
