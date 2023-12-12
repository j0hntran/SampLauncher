import os
import requests
import winreg
import json
import time
import webbrowser
from hashlib import sha256
thoigian = time.ctime()
user = os.getlogin()
date = time.ctime()
launcher_version = "1.1"
def check_for_update():
    response = requests.get("https://raw.githubusercontent.com/luuhoangductri/SampLauncher/main/update.json")
    if response.status_code == 200:
        version = response.json()
    else:
        print(f"Lỗi khi kiểm tra cập nhật, mã phản hồi:{response.status_code}")
    if launcher_version == version[0]:
        print("Bạn đang ở phiên bản mới nhất!")
    else:
        print(f"Phiên bản launcher hiện tại đang cũ. Phiên bản mới nhất đang là {version[0]}")
        print("Tiến hành lấy liên kết tải xuống.")
        print(f"Tiến hành mở liên kết: {version[1]}")
        webbrowser.open(version[1])
        quit()



def check_and_download_files(folder_path):
    if not os.path.exists(folder_path):
        print(f"Thư mục {folder_path} không tồn tại.")
        print(f"Tiến hành tạo thư mục {folder_path}.")
        os.mkdir("C:/Users/"+user+"/Documents/GTA San Andreas User Files/SAMP/cache/15.235.197.168.7777")

    files_in_folder = os.listdir(folder_path)

    response = requests.get("https://raw.githubusercontent.com/luuhoangductri/SampLauncher/main/cache.json")
    if response.status_code == 200:
        required_files = response.json()
        fileneeddownload = len(required_files)-len(files_in_folder)
        print(f"Số cache cần download: {fileneeddownload}")
    else:
        print(f"Lỗi khi lấy danh sách cache từ máy chủ. Mã trạng thái: {response.status_code}")
        return
    
    files_to_download = [file_name for file_name in required_files if file_name not in files_in_folder]

    if files_to_download:
        for file_name in files_to_download:
            download_url = f"https://raw.githubusercontent.com/luuhoangductri/SampLauncher/main/cachetest/{file_name}"
            download_path = os.path.join(folder_path, file_name)

            response = requests.get(download_url)
            if response.status_code == 200:
                with open(download_path, 'wb') as file:
                    file.write(response.content)
                print(f"Tải cache {file_name} thành công.")
            else:
                print(f"Lỗi khi tải cache {file_name} từ máy chủ. Mã trạng thái: {response.status_code}")
                error_output = "Tải cache thất bại từ URL: https://raw.githubusercontent.com/luuhoangductri/SampLauncher/main/cachetest/{}\n{}\n<@389385604598726657>".format(file_name,date)
                send_discord_webhook(error_output)
    else:
        print("Không có file nào thiếu.")

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
    except requests.exceptions.RequestException as e:
        print(f"Failed to send webhook: {e}")

if __name__ == "__main__":
    check_for_update()
    game_directory = r"."
    print(f"Đường dẫn game của bạn: {game_directory}")
    print("Đường dẫn cache của bạn: C:/Users/"+user+"/Documents/GTA San Andreas User Files/SAMP/cache/")
    print("Tiến hành kiểm tra thư mục...")
    json_url = "https://raw.githubusercontent.com/luuhoangductri/SampLauncher/main/checksums.json"

    stored_checksums = fetch_json_from_url(json_url)

    if stored_checksums is not None:
        matching_files = scan_and_compare(game_directory, stored_checksums)
        path = winreg.HKEY_CURRENT_USER
        path_a = winreg.OpenKeyEx(path, r"SOFTWARE\\SAMP\\")
        player = winreg.QueryValueEx(path_a, "PlayerName")
        if path_a:
            winreg.CloseKey(path_a)
        if matching_files:
            for file_path in matching_files:
                    message = "**Cleo detected!.**\nFilepath: {}\nIC: {}\nTime: {}".format(file_path,player[0],thoigian)
                    send_discord_webhook(message)
    print("Kiểm tra hoàn tất, tiến hành tải xuống cache.")
    check_and_download_files("C:/Users/"+user+"/Documents/GTA San Andreas User Files/SAMP/cache/15.235.197.168.7777")    