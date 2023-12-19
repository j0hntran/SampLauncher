import os
import json

def get_file_info(directory_path):
    file_info_list = []

    for filename in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, filename)):
            name, extension = os.path.splitext(filename)
            
            file_info_list.append(f"{name}{extension}")

    return file_info_list

def save_to_json(file_info, output_file):
    with open(output_file, 'w') as json_file:
        json.dump(file_info, json_file, indent=4)

if __name__ == "__main__":
    directory_path = "D:\Project/15.235.197.168.7777"

    file_info = get_file_info(directory_path)

    output_file = 'file_info.json'
    save_to_json(file_info, output_file)

    print(f"Thông tin đã được lưu vào tệp {output_file}")
