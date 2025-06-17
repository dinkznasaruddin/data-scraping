import kaggle
import pandas as pd
import os
import zipfile

# --- Deskripsi Skrip ---
# Skrip ini berfungsi untuk mengunduh dataset 'House Prices' dari Kaggle,
# mengekstrak file CSV yang diperlukan, dan memuatnya ke dalam DataFrame pandas.

# 1. Autentikasi ke API Kaggle (pastikan kaggle.json sudah ada)
print("Mengautentikasi ke API Kaggle...")
kaggle.api.authenticate()
print("Autentikasi berhasil.")

# 2. Nama dataset dan path tujuan
dataset_slug = 'house-prices-advanced-regression-techniques'
download_path = './data'

# Membuat direktori jika belum ada
if not os.path.exists(download_path):
    os.makedirs(download_path)

# 3. Mengunduh file dataset
print(f"Mengunduh dataset '{dataset_slug}' ke folder '{download_path}'...")
kaggle.api.competition_download_files(dataset_slug, path=download_path)
print("Unduhan selesai.")

# 4. Mengekstrak file zip
zip_file_path = os.path.join(download_path, dataset_slug + '.zip')
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extract('train.csv', path=download_path) # Hanya ekstrak train.csv
    print("File 'train.csv' berhasil diekstrak.")

# 5. Memuat data ke dalam DataFrame dan menampilkan hasilnya
csv_path = os.path.join(download_path, 'train.csv')
df = pd.read_csv(csv_path)

# Hasil: Menampilkan 5 baris pertama dari data yang berhasil diambil
print("\n--- Hasil Pengambilan Data (5 Baris Pertama) ---")
print(df.head())

# Menampilkan informasi dasar dari data
print("\n--- Informasi Data ---")
df.info()