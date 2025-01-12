import os
import requests

def download_file(url, dest_path):
    response = requests.get(url)
    with open(dest_path, 'wb') as f:
        f.write(response.content)

def check_and_update():
    base_url = "https://raw.githubusercontent.com/bol-van/zapret-win-bundle/refs/heads/master/zapret-winws/"

    files_to_check = [
        "cygwin1.dll",
        "quic_initial_www_google_com.bin",
        "tls_clienthello_www_google_com.bin",
        "WinDivert.dll",
        "WinDivert64.sys",
        "winws.exe"
    ]

    bin_path = 'bin'
    os.makedirs(bin_path, exist_ok=True)

    for file in files_to_check:
        file_path = os.path.join(bin_path, file)
        download_file(base_url + file, file_path)