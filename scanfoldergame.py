import os
import json
import requests
from hashlib import sha256

def calculate_sha256(file_path):
    sha256_hash = sha256()
    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def fetch_json_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Nếu có lỗi, nó sẽ ném một ngoại lệ
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch JSON from {url}: {e}")
        return None

def scan_and_compare(game_directory, checksums):
    matching_files = []

    for root, _, files in os.walk(game_directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            current_checksum = calculate_sha256(file_path)

            if current_checksum in checksums:
                matching_files.append(file_path)

    return matching_files

if __name__ == "__main__":
    game_directory = r"C:\path\to\your\game"
    json_url = "https://example.com/path/to/checksums.json"

    # Lấy giá trị SHA-256 trực tiếp từ URL
    stored_checksums = fetch_json_from_url(json_url)

    if stored_checksums is not None:
        # Quét thư mục trò chơi và so sánh giá trị SHA-256
        matching_files = scan_and_compare(game_directory, stored_checksums)

        if matching_files:
            print("Các tệp trùng khớp:")
            for file_path in matching_files:
                print(file_path)
        else:
            print("Không có tệp trùng khớp.")
