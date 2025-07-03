# example.py

import pandas as pd
import numpy as np
import proprep

# --- PENGGUNAAN 1: MEMANGGIL FUNGSI SECARA LANGSUNG ---
print("--- Menjalankan Fungsi Data Preparation ---")

# Buat DataFrame contoh
data = {'A': [1, 2, np.nan, 4], 'B': ['x', 'y', 'x', np.nan]}
df = pd.DataFrame(data)
print("Data Awal:")
print(df)

# Gunakan fungsi dari library Anda
df_clean = proprep.clean_and_encode_dataframe(
    df,
    numeric_strategy='Median',
    categorical_impute_strategy='Modus (Paling Sering Muncul)'
)
print("\nData Setelah Dibersihkan:")
print(df_clean)


# --- PENGGUNAAN 2: MELUNCURKAN APLIKASI EKSPERIMENTASI ---
print("\n--- Meluncurkan Aplikasi Gradio ---")
print("Tutup aplikasi (Ctrl+C di terminal) untuk melanjutkan.")

# Cukup panggil fungsi ini untuk menjalankan seluruh UI
proprep.launch_app()

print("\nSelesai.")