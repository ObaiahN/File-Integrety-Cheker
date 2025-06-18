import hashlib
import os

def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

def save_hashes(file_list, output_file):
    """Save file hashes to a reference file."""
    with open(output_file, 'w') as f:
        for file in file_list:
            file_hash = calculate_hash(file)
            if file_hash:
                f.write(f"{file}|{file_hash}\n")
    print(f"Hashes saved to {output_file}")

def verify_integrity(reference_file):
    """Check current file hashes against stored hashes."""
    if not os.path.exists(reference_file):
        print("Reference file not found.")
        return

    with open(reference_file, 'r') as f:
        for line in f:
            file_path, original_hash = line.strip().split('|')
            current_hash = calculate_hash(file_path)
            if not current_hash:
                continue
            if current_hash == original_hash:
                print(f"[OK] {file_path}")
            else:
                print(f"[MODIFIED] {file_path} ⚠️")

# Example usage:
if __name__ == "__main__":
    files_to_check = ['example.txt', 'data.csv']  # Replace with your files
    hash_file = 'hashes.txt'

    # First time: generate and save hashes
    save_hashes(files_to_check, hash_file)

    # Later: verify file integrity
    verify_integrity(hash_file)

