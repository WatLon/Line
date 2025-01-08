import sys
import configparser
import os
import subprocess
import shutil
import psutil
import winreg
import tempfile

def toggle_connection(state):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == 'winws.exe':
            if not state:
                proc.terminate()
                return
            elif state:
                proc.terminate()
                break
    else:
        if state:
            start_winws()

def start_winws():
    os.system('@echo off')
    os.system('chcp 65001 >nul')
    temp_dir = tempfile.gettempdir()
    zapret_dir = os.path.join(temp_dir, 'zapret')
    scr_dir = os.path.join(zapret_dir, 'scr')
    bin_dir = os.path.join(scr_dir, 'bin')
    os.environ['BIN'] = bin_dir
    os.environ['SCR'] = scr_dir
    config = configparser.RawConfigParser()
    config.read(os.path.join(scr_dir, 'config.cfg'))

    command_template = config.get("Winws", "command")
    command = command_template.replace("%BIN%", bin_dir + os.sep)
    command = command.replace("%SCR%", scr_dir + os.sep)
    command = command.split()

    subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)

def set_autostart(state):
    script_path = os.path.abspath(sys.argv[0])
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
    if state:
        winreg.SetValueEx(key, "Line - bypass dpi", 0, winreg.REG_SZ, script_path)
    else:
        try:
            winreg.DeleteValue(key, "Line - bypass dpi")
        except FileNotFoundError:
            pass

    winreg.CloseKey(key)

def select_config(file_path):
    temp_dir = tempfile.gettempdir()
    zapret_dir = os.path.join(temp_dir, 'zapret')
    scr_dir = os.path.join(zapret_dir, 'scr')
    file_name = os.path.basename(file_path)

    if file_name.endswith('.cfg'):
        config_path = os.path.join(scr_dir, 'config.cfg')
        if os.path.exists(config_path):
            os.remove(config_path)
        shutil.copy(file_path, config_path)
    elif file_name.startswith('ipset-') and file_name.endswith('.txt'):
        ipset_path = os.path.join(scr_dir, 'ipset-discord.txt')
        if os.path.exists(ipset_path):
            os.remove(ipset_path)
        shutil.copy(file_path, ipset_path)
    elif file_name.startswith('list-') and file_name.endswith('.txt'):
        list_path = os.path.join(scr_dir, 'list-general.txt')
        if os.path.exists(list_path):
            os.remove(list_path)
        shutil.copy(file_path, list_path)
    else:
        pass
