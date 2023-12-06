import hashlib
import os
import json

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_checksums(directory):
    checksums = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            checksum = calculate_sha256(file_path)
            checksums.append(checksum)
    return checksums

if __name__ == "__main__":
    target_directory = r"D:/Download/Modpak/cleo"
    output_json_file = "checksums.json"

    checksums = generate_checksums(target_directory)

    with open(output_json_file, "w") as json_file:
        json.dump(checksums, json_file, indent=2)

    print(f"Checksums saved to {output_json_file}")
