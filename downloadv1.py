import os
import requests
user = os.getlogin()
folder_path = "C:/Users/"+user+"/Documents/GTA San Andreas User Files/SAMP/cache"

def check_and_download_files(folder_path, host_url):
    # Kiểm tra xem thư mục có tồn tại không
    if not os.path.exists(folder_path):
        print(f"Thư mục {folder_path} không tồn tại.")
        return

    # Lấy danh sách các tệp trong thư mục
    files_in_folder = os.listdir(folder_path)

    # Danh sách các file cần tải từ máy chủ
    files_to_download = []

    # Ví dụ: Giả sử các file cần phải tồn tại là file1.txt và file2.txt
    required_files = ["file1.txt", "file2.txt"]

    for file_name in required_files:
        if file_name not in files_in_folder:
            files_to_download.append(file_name)

    # Tải các file thiếu từ máy chủ
    if files_to_download:
        print(f"Các file cần tải: {files_to_download}")
        for file_name in files_to_download:
            download_url = f"{host_url}/{file_name}"
            download_path = os.path.join(folder_path, file_name)

            # Tải file từ máy chủ
            response = requests.get(download_url)
            if response.status_code == 200:
                with open(download_path, 'wb') as file:
                    file.write(response.content)
                print(f"Tải file {file_name} thành công.")
            else:
                print(f"Lỗi khi tải file {file_name} từ máy chủ. Mã trạng thái: {response.status_code}")
    else:
        print("Không có file nào thiếu.")

# Sử dụng hàm
check_and_download_files(folder_path, "http://url-may-chu.com")
