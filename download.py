import requests
from tqdm import tqdm
import json
import time
import random
import os
import zipfile
errorcode = "ERROR-"+str(random.randint(0,999))
date = time.ctime()
user = os.getlogin()
print(user)
destination_folder = "C:/Users/"+user+"/Documents/GTA San Andreas User Files/SAMP/cache"

url = 'https://cdn.discordapp.com/attachments/1181825492475715585/1182197416187932702/15.235.197.168.7777.zip'
destination_path = "15.235.197.168.7777.zip"

response = requests.get(url, stream=True)
print("Tiến hành kiểm tra đường dẫn.")
def send_discord_webhook(message):
    payload = {"content": message}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post("https://discord.com/api/webhooks/1182190368821891103/3uO721aJTGGWz_GcPHbP9ZRFAewFC8FDoIHPLqjXdoqArrTz_6NmlmmZzs5MPYk1YJ98", data=json.dumps(payload), headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send webhook: {e}")
if response.status_code == 200:
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

    with open(destination_path, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()
    os.system('cls')
    print(f'Tải về thành công: {destination_path}')
    try:
        with zipfile.ZipFile('15.235.197.168.7777.zip', 'r') as zip_ref:
            zip_ref.extractall(destination_folder)

        print(f'Đã giải nén vào: {destination_folder}')
    except:
        error_output = "Giải nén thất bại từ URL: {}\n{}\nError Code: {}\n<@389385604598726657>".format(url,date,errorcode)
        send_discord_webhook(error_output)

else:
    print('Lỗi khi tải về. Error code: {}'.format(errorcode))
    error_output = "Tải về thất bại từ URL: {}\n{}\nError Code: {}\n<@389385604598726657>".format(url,date,errorcode)
    send_discord_webhook(error_output)
