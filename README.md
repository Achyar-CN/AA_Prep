# ProPrep 🚀

Supercharge alur kerja persiapan data Anda\! Dikembangkan oleh tim **Advanced Analytics**, **ProPrep** adalah *library* Python yang dirancang untuk mengubah data mentah yang berantakan menjadi dataset yang siap untuk *machine learning* dengan standarisasi dan efisiensi.

ProPrep menyediakan **dua mode utama**:

1.  **Library Mode**: Gunakan kumpulan fungsi *data preparation* yang kuat dan fleksibel langsung di dalam *notebook* atau skrip Anda.
2.  **App Mode**: Luncurkan aplikasi web interaktif dengan Gradio untuk bereksperimen dengan berbagai teknik *data preparation* secara visual dan *real-time*.

*(Tips: Anda bisa merekam layar aplikasi Gradio Anda dan mengubahnya menjadi GIF untuk ditaruh di sini)*

-----

## ✨ Fitur Utama

  * **Penanganan Nilai Hilang**: Isi nilai `NaN` dengan berbagai strategi (Mean, Median, Modus, Konstanta, KNN Imputer).
  * **Encoding Kategorikal**: Konversi variabel kategorikal menggunakan berbagai metode canggih (One-Hot, Ordinal, Frequency, Binary, Hashing).
  * **Penanganan Outlier**: Atasi nilai-nilai ekstrim dengan metode *IQR capping*.
  * **UI Eksperimental**: Antarmuka Gradio yang intuitif untuk validasi visual dan statistik dari setiap langkah pemrosesan.
  * **Modular & Dapat Digunakan Kembali**: Desain yang bersih memungkinkan Anda mengimpor fungsionalitas inti ke proyek apa pun.

-----

## ⚙️ Instalasi

1.  **Clone Repositori**

    ```bash
    git clone https://github.com/your-username/proprep_project.git
    cd proprep_project
    ```

2.  **Instal Dependensi**
    Pastikan Anda berada di direktori utama proyek, lalu jalankan:

    ```bash
    pip install -r requirements.txt
    ```

-----

## 🚀 Quick Start

Gunakan `proprep` dengan sangat mudah dalam dua cara.

### 1\. Sebagai Library di Skrip Python

Impor dan gunakan `clean_and_encode_dataframe` untuk memproses data Anda secara langsung.

```python
# example.py
import pandas as pd
import numpy as np
import proprep

# Buat DataFrame contoh
data = {
    'age': [25, 30, np.nan, 45, 22],
    'city': ['New York', 'London', 'Paris', 'New York', np.nan],
    'gender': ['M', 'F', 'F', 'M', 'M']
}
df = pd.DataFrame(data)
print("Data Awal:\n", df)

# Proses data dengan ProPrep
df_clean = proprep.clean_and_encode_dataframe(
    df,
    numeric_strategy='Median',
    categorical_impute_strategy='Modus (Paling Sering Muncul)',
    categorical_encoding_strategy='One-Hot Encoding',
    cols_to_encode=['city', 'gender']
)

print("\nData Siap untuk Model:\n", df_clean)
```

### 2\. Sebagai Aplikasi Eksperimen Interaktif

Luncurkan aplikasi Gradio hanya dengan satu baris kode.

```python
# launch_ui.py
import proprep

# Ini akan membuka aplikasi di browser Anda
proprep.launch_app()
```

-----

## 🔧 Komponen Inti

  * `proprep.clean_and_encode_dataframe()`: Fungsi utama yang menerima DataFrame dan serangkaian opsi konfigurasi, lalu mengembalikan DataFrame yang telah diproses.
  * `proprep.create_comparison_viz_and_stats()`: Fungsi untuk membuat visualisasi perbandingan dan tabel statistik (digunakan secara internal oleh aplikasi).
  * `proprep.launch_app()`: Fungsi untuk meluncurkan antarmuka pengguna Gradio.

-----

## 🤝 Berkontribusi

Kontribusi Anda sangat kami harapkan\! Jika Anda memiliki ide untuk fitur baru atau menemukan bug, silakan buka *issue* atau kirimkan *pull request*.

1.  *Fork* repositori ini.
2.  Buat *branch* baru (`git checkout -b feature/AmazingFeature`).
3.  *Commit* perubahan Anda (`git commit -m 'Add some AmazingFeature'`).
4.  *Push* ke *branch* Anda (`git push origin feature/AmazingFeature`).
5.  Buka *Pull Request*.

-----

## 📜 Lisensi

Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk detail lebih lanjut.

-----

***Happy Data Prepping\!***