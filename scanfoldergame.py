import os
import requests
import winreg
import json
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
        response.raise_for_status()
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
def send_discord_webhook(message):
    payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post("https://discord.com/api/webhooks/1181825984408850473/WjajVKE_In1lYb8ZYbvNw1ukL3GZvSBlHxfJ-RjMNxu6W5rPwuipT8INiD3HVsVPQN4F", data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print("Webhook sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send webhook: {e}")

if __name__ == "__main__":
    game_directory = r"D:/Download/Modpak/cleo"
    json_url = "https://raw.githubusercontent.com/luuhoangductri/SampLauncher/main/checksums.json"

    stored_checksums = fetch_json_from_url(json_url)

    if stored_checksums is not None:
        matching_files = scan_and_compare(game_directory, stored_checksums)

        if matching_files:
            path = winreg.HKEY_CURRENT_USER
            path_a = winreg.OpenKeyEx(path, r"SOFTWARE\\SAMP\\")
            player = winreg.QueryValueEx(path_a, "PlayerName")
            if path_a:
                winreg.CloseKey(path_a)
            print("Các tệp trùng khớp:")
            for file_path in matching_files:
                print(file_path)
                message = "Cleo detected:{}\nIC:{}".format(file_path,player[0])
                send_discord_webhook(message)
            
            
        else:
            print("Không có tệp trùng khớp.")
            os.system("D:/Download/Modpak/Zin/samp.exe 51.254.139.153:7777")