#!/usr/bin/env python3
# Modern LK Patcher for MTK Devices (Fastboot & Bootloader Unlock)
# Referensi: https://github.com/R0rt1z2/lkpatcher
# Fitur: Menu interaktif, clean project (auto hapus semua .json), auto dependency check, auto clear terminal, loading animasi
# Instalasi: pkg install python; pip install --upgrade git+https://github.com/R0rt1z2/lkpatcher tqdm
# Penggunaan: python3 lkpatcher_modern.py

import sys
import os
import time
import json
import subprocess
import importlib.util
import shutil
import glob
from datetime import datetime
from lkpatcher.patcher import LkPatcher
from lkpatcher.config import PatcherConfig
from tqdm import tqdm

# Warna untuk tampilan modern
class Colors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Variabel global untuk menyimpan nama file patch terakhir
last_patched_file = None

def clear_terminal():
    """Bersihkan terminal sebelum menjalankan script."""
    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{Colors.CYAN}Terminal dibersihkan untuk tampilan baru!{Colors.END}\n")

def check_and_install_package(package_name, install_command=None):
    """Cek apakah package sudah terinstall, instal jika belum."""
    if package_name == 'lkpatcher':
        spec = importlib.util.find_spec('lkpatcher')
        if spec is not None:
            print(f"{Colors.GREEN}{package_name} sudah terinstall, melewati instalasi.{Colors.END}")
            return
    else:
        try:
            __import__(package_name)
            print(f"{Colors.GREEN}{package_name} sudah terinstall, melewati instalasi.{Colors.END}")
            return
        except ImportError:
            pass
    
    print(f"{Colors.YELLOW}Menginstall {package_name}...{Colors.END}")
    if install_command:
        subprocess.check_call(install_command)
    else:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    print(f"{Colors.GREEN}{package_name} berhasil terinstall!{Colors.END}")

def install_dependencies():
    """Cek dan instal dependencies jika belum terinstall."""
    print(f"{Colors.YELLOW}Memeriksa dependencies...{Colors.END}")
    check_and_install_package('tqdm')
    check_and_install_package('lkpatcher', [sys.executable, "-m", "pip", "install", "--upgrade", "git+https://github.com/R0rt1z2/lkpatcher"])

def print_banner():
    """Tampilkan banner keren."""
    print(f"{Colors.CYAN}{Colors.BOLD}========================================={Colors.END}")
    print(f"{Colors.CYAN}       MTK LK Patcher - Fastboot Unlock  {Colors.END}")
    print(f"{Colors.CYAN}       Powered by lkpatcher (R0rt1z2)    {Colors.END}")
    print(f"{Colors.CYAN}       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}         {Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}========================================={Colors.END}\n")

def loading_animation(message, duration=3):
    """Animasi loading dengan progress bar."""
    print(f"{Colors.YELLOW}{message}{Colors.END}")
    for _ in tqdm(range(100), desc="Loading", bar_format="{l_bar}{bar} {r_bar}", ncols=50):
        time.sleep(duration / 100)
    print()

def create_default_patches_json():
    """Buat file patches.json default untuk fastboot dan dm_verity."""
    patches = {
        "mode": "update",
        "fastboot": {
            "2de9f04fadf5ac5d": "00207047"  # Contoh patch untuk fastboot
        },
        "dm_verity": {
            "30b583b002ab0022": "00207047"  # Contoh patch untuk dm_verity
        }
    }
    with open('patches.json', 'w') as f:
        json.dump(patches, f, indent=4)
    print(f"{Colors.GREEN}File patches.json dibuat.{Colors.END}")

def create_default_config_json():
    """Buat file config.json default."""
    config_data = {
        "log_level": "INFO",
        "backup": True,
        "backup_dir": "./backups",
        "verify_patch": True,
        "allow_incomplete": True,
        "dry_run": False,
        "patch_categories": ["fastboot", "dm_verity"],
        "exclude_categories": []
    }
    os.makedirs('backups', exist_ok=True)
    with open('config.json', 'w') as f:
        json.dump(config_data, f, indent=4)
    print(f"{Colors.GREEN}File config.json dibuat.{Colors.END}")

def clean_project():
    """Hapus semua file .json, backup, dan file patch untuk clean total."""
    global last_patched_file
    print(f"{Colors.YELLOW}Membersihkan project...{Colors.END}")
    
    # Hapus semua file .json di direktori saat ini
    json_files = glob.glob('*.json')
    for file in json_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"{Colors.GREEN}File {file} dihapus.{Colors.END}")
        else:
            print(f"{Colors.YELLOW}File {file} tidak ditemukan, dilewati.{Colors.END}")
    
    # Hapus file patch terakhir jika ada
    if last_patched_file and os.path.exists(last_patched_file):
        os.remove(last_patched_file)
        print(f"{Colors.GREEN}File {last_patched_file} dihapus.{Colors.END}")
    elif last_patched_file:
        print(f"{Colors.YELLOW}File {last_patched_file} tidak ditemukan, dilewati.{Colors.END}")
    
    # Hapus folder backups
    folders_to_clean = ['backups']
    for folder in folders_to_clean:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"{Colors.GREEN}Folder {folder} dihapus.{Colors.END}")
        else:
            print(f"{Colors.YELLOW}Folder {folder} tidak ditemukan, dilewati.{Colors.END}")
    
    last_patched_file = None  # Reset nama file patch
    loading_animation("Project berhasil dibersihkan!")
    print(f"{Colors.GREEN}Project telah direset ke keadaan awal.{Colors.END}")

def patch_lk_partition():
    """Proses patching LK partition."""
    global last_patched_file
    # Ambil input pengguna
    print(f"{Colors.CYAN}{Colors.BOLD}=== Input File ==={Colors.END}")
    input_img = input(f"{Colors.YELLOW}Masukkan nama target file (contoh: lk.img): {Colors.END}").strip()
    output_img = input(f"{Colors.YELLOW}Masukkan nama patch file (contoh: lk_patched.img): {Colors.END}").strip()

    # Validasi input
    if not input_img or not output_img:
        print(f"{Colors.RED}Error: Nama file tidak boleh kosong!{Colors.END}")
        return
    if not os.path.exists(input_img):
        print(f"{Colors.RED}Error: File {input_img} tidak ditemukan!{Colors.END}")
        return

    # Simpan nama file patch
    last_patched_file = output_img

    # Buat file konfigurasi
    loading_animation("Mempersiapkan file konfigurasi...")
    create_default_patches_json()
    create_default_config_json()

    # Load config
    config = PatcherConfig()
    with open('config.json', 'r') as f:
        config_data = json.load(f)
    config.log_level = config_data['log_level']
    config.backup = config_data['backup']
    config.patch_categories = set(config_data['patch_categories'])

    # Inisialisasi patcher
    print(f"{Colors.YELLOW}Memulai proses patching...{Colors.END}")
    patcher = LkPatcher(
        image=input_img,
        patches='patches.json',
        config=config
    )

    # Proses patching dengan progress bar
    try:
        with tqdm(total=100, desc="Patching", bar_format="{l_bar}{bar} {r_bar}", ncols=50) as pbar:
            output_path = patcher.patch(output=output_img)
            for _ in range(100):
                time.sleep(0.05)  # Simulasi proses
                pbar.update(1)
        print(f"{Colors.GREEN}Patching selesai! Output: {output_path}{Colors.END}")

        # Analisis hasil
        loading_animation("Menganalisis image...")
        analysis = patcher.analyze_image()
        print(f"{Colors.CYAN}Hasil analisis image:{Colors.END}")
        print(analysis)

        print(f"\n{Colors.GREEN}{Colors.BOLD}Proses selesai! File patched: {output_img}{Colors.END}")
        print(f"{Colors.CYAN}Flash file menggunakan mtkclient atau tool lain.{Colors.END}")

    except Exception as e:
        print(f"{Colors.RED}Error saat patching: {e}{Colors.END}")

def show_menu():
    """Tampilkan menu interaktif."""
    print(f"{Colors.CYAN}{Colors.BOLD}=== Menu LK Patcher ==={Colors.END}")
    print(f"{Colors.YELLOW}1. Patch LK Partition{Colors.END}")
    print(f"{Colors.YELLOW}2. Clean Project{Colors.END}")
    print(f"{Colors.YELLOW}3. Exit{Colors.END}")
    choice = input(f"{Colors.CYAN}Pilih opsi (1-3): {Colors.END}").strip()
    return choice

def main():
    # Bersihkan terminal
    clear_terminal()

    # Tampilkan banner
    print_banner()

    # Cek dan instal dependencies
    install_dependencies()

    # Loop menu hingga user memilih exit
    while True:
        clear_terminal()
        print_banner()
        choice = show_menu()

        if choice == '1':
            clear_terminal()
            print_banner()
            patch_lk_partition()
            input(f"\n{Colors.CYAN}Tekan Enter untuk kembali ke menu...{Colors.END}")
        elif choice == '2':
            clear_terminal()
            print_banner()
            clean_project()
            input(f"\n{Colors.CYAN}Tekan Enter untuk kembali ke menu...{Colors.END}")
        elif choice == '3':
            print(f"{Colors.GREEN}Keluar dari program. Terima kasih!{Colors.END}")
            break
        else:
            print(f"{Colors.RED}Pilihan tidak valid! Pilih 1, 2, atau 3.{Colors.END}")
            input(f"{Colors.CYAN}Tekan Enter untuk kembali ke menu...{Colors.END}")

if __name__ == "__main__":
    main()
