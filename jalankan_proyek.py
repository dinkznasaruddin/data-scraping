import kaggle
import pandas as pd
import sqlite3
import os
import zipfile

# --- BAGIAN 1: PENGATURAN PROYEK ---
# Definisikan semua nama dan path yang akan digunakan
COMPETITION_SLUG = 'house-prices-advanced-regression-techniques'
DOWNLOAD_PATH = './data_proyek'  # Nama folder untuk menyimpan semua file
DB_PATH = os.path.join(DOWNLOAD_PATH, 'house_prices.db') # Path lengkap ke file database
TABLE_NAME = 'harga_rumah_training'
CSV_FILE_NAME = 'train.csv'

# --- BAGIAN 2: PENGAMBILAN DATA (TUGAS 2) ---
print("--- Memulai Proses Pengambilan Data (Tugas 2) ---")

# 1. Autentikasi ke API Kaggle (membaca file kaggle.json)
try:
    print("1. Mengautentikasi ke API Kaggle...")
    kaggle.api.authenticate()
    print("   -> Autentikasi berhasil.")
except Exception as e:
    print(f"   -> GAGAL: Tidak bisa autentikasi. Pastikan kaggle.json ada di ~/.kaggle/kaggle.json atau C:\\Users\\<User>\\.kaggle\\kaggle.json. Error: {e}")
    exit() # Hentikan skrip jika autentikasi gagal

# 2. Membuat direktori tujuan jika belum ada
if not os.path.exists(DOWNLOAD_PATH):
    print(f"2. Membuat folder tujuan di: {DOWNLOAD_PATH}")
    os.makedirs(DOWNLOAD_PATH)
else:
    print(f"2. Folder tujuan '{DOWNLOAD_PATH}' sudah ada.")

# 3. Mengunduh file dataset dari kompetisi Kaggle
print(f"3. Mengunduh dataset '{COMPETITION_SLUG}'...")
kaggle.api.competition_download_files(COMPETITION_SLUG, path=DOWNLOAD_PATH)
print("   -> Unduhan selesai.")

# 4. Mengekstrak file CSV yang relevan dari file ZIP
zip_file_path = os.path.join(DOWNLOAD_PATH, COMPETITION_SLUG + '.zip')
print(f"4. Mengekstrak '{CSV_FILE_NAME}' dari file zip...")
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extract(CSV_FILE_NAME, path=DOWNLOAD_PATH)
print(f"   -> File '{CSV_FILE_NAME}' berhasil diekstrak.")
print("--- Proses Pengambilan Data Selesai ---\n")


# --- BAGIAN 3: INTEGRASI DATA KE DATABASE (TUGAS 3) ---
print("--- Memulai Proses Integrasi Database (Tugas 3) ---")
try:
    # 1. Membaca data dari file CSV ke dalam pandas DataFrame
    csv_path = os.path.join(DOWNLOAD_PATH, CSV_FILE_NAME)
    print(f"1. Membaca data dari '{csv_path}'...")
    df = pd.read_csv(csv_path)
    print(f"   -> Berhasil memuat {len(df)} baris data.")

    # 2. Membuat koneksi ke database SQLite
    print(f"2. Menghubungkan ke database di '{DB_PATH}'...")
    conn = sqlite3.connect(DB_PATH)
    print("   -> Koneksi database berhasil.")

    # 3. Mengunggah data dari DataFrame ke tabel di database
    print(f"3. Mengunggah data ke tabel '{TABLE_NAME}'...")
    # if_exists='replace' akan menghapus tabel lama jika ada dan menggantinya dengan yang baru
    df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
    print("   -> Data berhasil diunggah.")

    # 4. Verifikasi bahwa data sudah benar-benar masuk
    print("4. Melakukan verifikasi data di database...")
    df_from_db = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME} LIMIT 5", conn)
    print("   -> Verifikasi berhasil! Berikut 5 baris pertama dari tabel di database:")
    print(df_from_db)

except Exception as e:
    print(f"   -> GAGAL: Terjadi kesalahan saat proses integrasi database. Error: {e}")

finally:
    # 5. Menutup koneksi database
    if 'conn' in locals() and conn:
        conn.close()
        print("5. Koneksi database ditutup.")
    print("--- Proses Integrasi Database Selesai ---")