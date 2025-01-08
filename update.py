import os
import requests
import tempfile
from image import png1, png2
from fonts import Dot_Matrix_ttf, NType82_Regular_otf

def download_file(url, dest_path):
    response = requests.get(url)
    with open(dest_path, 'wb') as f:
        f.write(response.content)

def create_list_general_txt(file_path):
    content = """googlevideo.com
youtu.be
youtube.com
youtubei.googleapis.com
youtubeembeddedplayer.googleapis.com
ytimg.l.google.com
ytimg.com
jnn-pa.googleapis.com
youtube-nocookie.com
youtube-ui.l.google.com
yt-video-upload.l.google.com
wide-youtube.l.google.com
youtubekids.com
ggpht.com
discord.com
gateway.discord.gg
cdn.discordapp.com
discordapp.net
discordapp.com
discord.gg
media.discordapp.net
images-ext-1.discordapp.net
discord.app
discord.media
discordcdn.com
discord.dev
discord.new
discord.gift
discordstatus.com
dis.gd
discord.co
discord-attachments-uploads-prd.storage.googleapis.com
7tv.app
7tv.io
10tv.app
cloudflare-ech.com"""
    with open(file_path, 'w') as f:
        f.write(content)

def create_config_cfg(file_path):
    content = """[Winws]
command = %BIN%winws.exe --wf-tcp=80,443 --wf-udp=443,50000-50100 --filter-udp=443 --hostlist=%SCR%list-general.txt --dpi-desync=fake --dpi-desync-repeats=6 --dpi-desync-fake-quic=%BIN%quic_initial_www_google_com.bin --new --filter-udp=50000-50100 --ipset=%SCR%ipset-discord.txt --dpi-desync=fake --dpi-desync-any-protocol --dpi-desync-cutoff=d3 --dpi-desync-repeats=6 --new --filter-tcp=80 --hostlist=%SCR%list-general.txt --dpi-desync=fake,split2 --dpi-desync-autottl=2 --dpi-desync-fooling=md5sig --new --filter-tcp=443 --hostlist=%SCR%list-general.txt --dpi-desync=fake,split --dpi-desync-autottl=2 --dpi-desync-repeats=6 --dpi-desync-fooling=badseq --dpi-desync-fake-tls=%BIN%tls_clienthello_www_google_com.bin

[Autostart]
enabled = 0

[Autoupdate]
enabled = 0
"""
    with open(file_path, 'w') as f:
        f.write(content)

def check_and_update(update=True):
    base_url = "https://raw.githubusercontent.com/bol-van/zapret-win-bundle/refs/heads/master/zapret-winws/"

    files_to_check = [
        "cygwin1.dll",
        "quic_initial_www_google_com.bin",
        "tls_clienthello_www_google_com.bin",
        "WinDivert.dll",
        "WinDivert64.sys",
        "winws.exe"
    ]

    txt_files = [
        ("ipset-discord.txt", base_url + "ipset-discord.txt")
    ]

    temp_dir = tempfile.gettempdir()
    zapret_path = os.path.join(temp_dir, 'zapret', 'scr')
    bin_path = os.path.join(zapret_path, 'bin')
    os.makedirs(bin_path, exist_ok=True)

    if update:
        for file in files_to_check:
            file_path = os.path.join(bin_path, file)
            download_file(base_url + file, file_path)
    else:
        for file in files_to_check:
            file_path = os.path.join(bin_path, file)
            if not os.path.exists(file_path):
                download_file(base_url + file, file_path)

    for txt_file, url in txt_files:
        txt_file_path = os.path.join(zapret_path, txt_file)
        if not os.path.exists(txt_file_path):
            download_file(url, txt_file_path)

    list_general_txt_path = os.path.join(zapret_path, 'list-general.txt')
    if not os.path.exists(list_general_txt_path):
        create_list_general_txt(list_general_txt_path)

    config_cfg_path = os.path.join(zapret_path, 'config.cfg')
    if not os.path.exists(config_cfg_path):
        create_config_cfg(config_cfg_path)

    image_files = [(png1, '1.png'), (png2, '2.png')]
    for image_data, image_file in image_files:
        dest_path = os.path.join(zapret_path, image_file)
        if not os.path.exists(dest_path):
            with open(dest_path, 'wb') as dest_file:
                dest_file.write(image_data)

    font_files = [(Dot_Matrix_ttf, 'Dot-Matrix.ttf'), (NType82_Regular_otf, 'NType82-Regular.otf')]
    for font_data, font_file in font_files:
        dest_path = os.path.join(zapret_path, font_file)
        if not os.path.exists(dest_path):
            with open(dest_path, 'wb') as dest_file:
                dest_file.write(font_data)
