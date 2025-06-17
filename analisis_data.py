import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Path ke database yang sudah dibuat sebelumnya
DB_PATH = './data_proyek/house_prices.db'
TABLE_NAME = 'harga_rumah_training'

# Membuat koneksi ke database dan membaca data
try:
    conn = sqlite3.connect(DB_PATH)
    # Membaca seluruh data dari tabel ke dalam DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {TABLE_NAME}", conn)
    conn.close()
    print("✅ Data berhasil dimuat dari database.")
    print(f"   Jumlah baris: {df.shape[0]}, Jumlah kolom: {df.shape[1]}")
except Exception as e:
    print(f"❌ Gagal memuat data: {e}")
    exit()

# Mengatur agar plot ditampilkan dengan baik
plt.style.use('seaborn-v0_8-whitegrid')