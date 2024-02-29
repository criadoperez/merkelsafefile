import os
import sys
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, jsonify
from common.merkle import MerkleTree, hash_data

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
app = Flask(__name__)

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Ensure the storage directory exists
file_storage_path = "server_uploaded_files/"
os.makedirs(file_storage_path, exist_ok=True)

# Initialize a global Merkle tree and a dictionary to store file indices
global_merkle_tree = MerkleTree([])
file_indices = {}

def find_file_index(filename):
    # Assuming file_indices is a dictionary mapping filenames to their indices
    global file_indices  # If file_indices is a global variable
    return file_indices.get(filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = file.filename
        filepath = os.path.join(file_storage_path, filename)

        # Save the file before reading its content
        file.save(filepath)
        logging.info(f"File {filename} saved to {filepath}")

        # Compute file hash to confirm file content is saved
        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()
                file_hash = hash_data(file_data)
                logging.info(f"Computed hash for {filename}: {file_hash}")
        except Exception as e:
            logging.error(f"Error reading file {filepath}: {e}")
            return jsonify({"message": "Failed to read file for hashing"}), 500

        # Update the global Merkle tree with the new file hash
        global global_merkle_tree
        global_merkle_tree.add_leaf(file_hash)
        logging.info(f"File hash {file_hash} added to the Merkle tree.")

        return jsonify({"message": "File uploaded successfully", "hash": file_hash}), 200
    else:
        logging.warning("No file found in the request")
        return jsonify({"message": "No file found in the request"}), 400


@app.route('/request_file', methods=['GET'])
def request_file():
    filename = request.args.get('filename')
    filepath = os.path.join(file_storage_path, filename)

    if os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as f:
                file_data = f.read()
                file_hash = hash_data(file_data)
        except Exception as e:
            logging.error(f"Error reading file {filepath}: {e}")
            return jsonify({"message": "Failed to read file for hashing"}), 500

        # Generate proof using file_hash
        proof = global_merkle_tree.generate_proof(file_hash)

        return jsonify({
            "file_data": file_data.decode('utf-8'),
            "file_hash": file_hash,
            "proof": proof
        }), 200
    else:
        logging.error(f"File {filename} not found.")
        return jsonify({"message": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
