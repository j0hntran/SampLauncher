import os
import requests
user = os.getlogin()
def check_and_download_files(folder_path):
    
    if not os.path.exists(folder_path):
        print(f"Thư mục {folder_path} không tồn tại.")
        print(f"Tiến hành tạo thư mục {folder_path}.")
        os.mkdir("C:/Users/"+user+"/Documents/GTA San Andreas User Files/SAMP/cache/15.235.197.168.7777")

    files_in_folder = os.listdir(folder_path)

    response = requests.get("https://raw.githubusercontent.com/luuhoangductri/SampLauncher/main/cache.json")
    if response.status_code == 200:
        required_files = response.json()
    else:
        print(f"Lỗi khi lấy danh sách file từ máy chủ. Mã trạng thái: {response.status_code}")
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
                print(f"Tải file {file_name} thành công.")
            else:
                print(f"Lỗi khi tải file {file_name} từ máy chủ. Mã trạng thái: {response.status_code}")
    else:
        print("Không có file nào thiếu.")

check_and_download_files("C:/Users/"+user+"/Documents/GTA San Andreas User Files/SAMP/cache/15.235.197.168.7777")
