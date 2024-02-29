import hashlib

def hash_data(data):
    """Hashes the provided data using SHA-256."""
    hasher = hashlib.sha256()
    if isinstance(data, str):
        hasher.update(data.encode('utf-8'))
    elif isinstance(data, bytes):
        hasher.update(data)
    else:
        raise TypeError("hash_data expects a string or bytes object")
    return hasher.hexdigest()

class MerkleNode:
    """Represents a node in the Merkle tree."""
    def __init__(self, left=None, right=None, data=None, parent=None):
        self.left = left
        self.right = right
        self.parent = parent
        if left and right:  # Combine left and right node hashes
            # Consistent ordering for hash combination
            combined = hash_data(min(left.hash, right.hash) + max(left.hash, right.hash))
            self.hash = combined
        elif data is not None:  # Leaf node with data
            self.hash = data  # Use the provided hash directly if already hashed
        else:
            self.hash = None
        print(f"Node created: {self.hash}")  # Logging the hash of the node

class MerkleTree:
    """Represents a Merkle tree."""
    def __init__(self, data_list=[]):
        self.leaves = [MerkleNode(data=data) for data in data_list]
        self.root = self.build_tree(self.leaves) if data_list else None

    def add_leaf(self, leaf_hash):
        """Adds a new leaf to the tree."""
        new_leaf = MerkleNode(data=leaf_hash)
        self.leaves.append(new_leaf)
        print(f"Leaf added: {new_leaf.hash}")  # Logging the hash of the added leaf
        self.rebuild_tree()

    def rebuild_tree(self):
        """Rebuilds the Merkle tree based on the current leaves."""
        self.root = self.build_tree(self.leaves)
        print(f"Tree rebuilt. New root: {self.root.hash}")  # Logging the hash of the new root

    def build_tree(self, nodes):
        """Builds the Merkle tree from the leaves up."""
        if len(nodes) == 1:
            return nodes[0]
        new_level = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i + 1] if i + 1 < len(nodes) else left  # Duplicate the last node if necessary
            new_node = MerkleNode(left=left, right=right)
            left.parent = new_node  # Set parent reference for left
            right.parent = new_node  # Set parent reference for right
            new_level.append(new_node)
        return self.build_tree(new_level)

    def find_file_index(self, file_hash):
        for index, leaf in enumerate(self.leaves):
            if leaf.data == file_hash:
                return index
        return None

    def generate_proof(self, file_hash):
        """Generates a proof for the leaf with the specified hash."""
        print(f"Generating proof for file hash: {file_hash}")  # Debugging line
        proof = []
        # Find the leaf node with the matching hash
        for leaf in self.leaves:
            if leaf.hash == file_hash:
                current_node = leaf
                print(f"Leaf found: {current_node.hash}")  # Debugging line
                break
        else:
            print(f"No matching leaf found for hash: {file_hash}")  # Debugging line
            return proof  # Return empty proof if no matching leaf is found

        while current_node.parent:
            parent = current_node.parent
            sibling = parent.right if parent.left == current_node else parent.left
            proof.append(sibling.hash)
            current_node = parent

        return proof


    def verify_proof(self, leaf_hash, proof, root_hash):
        current_hash = leaf_hash
        for sibling_hash in proof:
            # Combine hashes in a consistent order
            combined = hash_data(min(current_hash, sibling_hash) + max(current_hash, sibling_hash))
            current_hash = combined
            print(f"Intermediate hash after combining with proof element: {current_hash}")  # Debugging line
            print(f"Computed root hash: {current_hash}")  # Debugging line
            print(f"Stored root hash: {root_hash}")  # Debugging line
        return current_hash == root_hash