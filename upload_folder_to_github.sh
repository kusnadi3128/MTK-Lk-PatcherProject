#!/bin/bash

# Script Universal untuk Upload Seluruh Isi Folder ke GitHub Secara Instan
# Kompatibel dengan Termux, Windows CMD/PowerShell, dan Linux distro
# Mengunggah semua file dan subfolder tanpa penentuan manual

echo "=== Tutorial dan Script Upload Folder ke GitHub ==="
echo "Langkah-langkah akan dijalankan otomatis dengan panduan."
echo "Pastikan Git terinstal. Jika belum, instal terlebih dahulu:"
echo "- Termux: 'pkg install git -y'"
echo "- Linux: 'sudo apt install git -y' (atau sesuai distro)"
echo "- Windows: Download Git dari https://git-scm.com dan instal"
echo "Tekan Enter untuk melanjutkan..."
read

# 1. Inisialisasi Git dan Konfigurasi
echo "1. Inisialisasi Git dan konfigurasi identitas..."
if [ ! -d ".git" ]; then
    git init -b main
    echo "Git diinisialisasi dengan branch default 'main'."
else
    echo "Git sudah diinisialisasi sebelumnya."
fi
echo "Atur nama dan email Git (digunakan untuk commit):"
read -p "Masukkan nama GitHub kamu (misal: kusnadi3128): " git_name
read -p "Masukkan email GitHub kamu (misal: kiolaazka@gmail.com): " git_email
git config user.name "$git_name"
git config user.email "$git_email"
git config --global --add safe.directory "$(pwd)"
echo "Identitas Git diatur: $git_name <$git_email>. Direktori ditambahkan ke safe.directory."

# 2. Tambahkan Semua File dan Commit
echo "2. Menambahkan semua file dan subfolder ke Git..."
git add .
echo "Semua file dan subfolder ditambahkan. Membuat commit awal..."
git commit -m "Initial commit: Upload all files from folder"
echo "Commit awal selesai."

# 3. Buat Repo di GitHub dan Push
echo "3. Membuat repository di GitHub dan push semua isi folder..."
read -p "Masukkan username GitHub kamu (misal: kusnadi3128): " github_user
echo "Buka https://github.com/new di browser, buat repo baru dengan nama bebas (misal: 'my-folder-upload')."
echo "Pilih 'Public', JANGAN centang 'Add a README file' untuk hindari konflik."
echo "Setelah dibuat, salin URL repo: https://github.com/$github_user/nama-repo.git"
read -p "Masukan URL repo (contoh: https://github.com/kusnadi3128/my-folder-upload.git): " repo_url
git remote add origin "$repo_url"
echo "Remote repo ditambahkan. Sekarang push ke GitHub:"
read -p "Masukkan Personal Access Token (PAT) dari GitHub (buat di Settings > Developer settings > Personal access tokens, scope 'repo'): " pat
git push https://"$github_user":"$pat"@github.com/"$github_user"/$(basename "$repo_url" .git).git main
echo "Semua file dan subfolder di-push ke GitHub. Verifikasi di: $repo_url"

# 4. Aktifkan GitHub Pages (Opsional, untuk situs statis)
echo "4. Mengaktifkan GitHub Pages (opsional, jika ingin situs live)..."
echo "Buka $repo_url/settings/pages di browser."
echo "Pilih 'Source: Deploy from a branch' > Branch: 'main' > Folder: '/ (root)' > Klik 'Save'."
echo "Tunggu 1-10 menit, lalu cek situs di: https://$github_user.github.io/$(basename "$repo_url" .git)/"
echo "Jika Pages tidak muncul, pastikan repo Public (Settings > General > Danger Zone)."

echo "=== Proses Selesai! ✅ ==="
echo "Semua isi folder telah di-upload ke GitHub di: $repo_url"
echo "Jika ada error, cek log di atas atau ulangi langkah yang gagal."