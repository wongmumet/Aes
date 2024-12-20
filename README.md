# S-Box Analysis Tool

## Deskripsi
Aplikasi ini merupakan alat untuk menganalisis sifat-sifat S-Box menggunakan beberapa parameter kriptografi seperti:

- **Nonlinearity (NL)**: Mengukur tingkat non-linearitas S-Box.
- **Strict Avalanche Criterion (SAC)**: Mengukur perubahan bit dalam output saat satu bit input diubah.
- **Linear Approximation Probability (LAP)**: Mengukur probabilitas bahwa kombinasi masukan menghasilkan keluaran linier tertentu.
- **Differential Approximation Probability (DAP)**: Mengukur probabilitas diferensial maksimum.
- **BIC Nonlinearity (BIC-NL)**: Mengukur non-linearitas independensi pasangan bit.
- **BIC Strict Avalanche Criterion (BIC-SAC)**: Mengukur SAC untuk independensi pasangan bit.

## Fitur
- **Upload File**: Mendukung pengunggahan file S-Box dalam format Excel (.xlsx, .xls).
- **Analisis Parameter**: Memilih parameter kriptografi untuk dihitung.
- **Hasil dalam Tabel**: Menampilkan hasil analisis dalam tabel.
- **Unduh Hasil**: Mendukung pengunduhan hasil analisis dalam format Excel.

## Instalasi
1. Pastikan Python sudah terinstal di perangkat Anda.
2. Install pustaka yang diperlukan dengan menjalankan perintah berikut:

```bash
pip install streamlit pandas numpy openpyxl xlsxwriter
```

3. Simpan file kode Python (misalnya `aes2.py`) di direktori pilihan Anda.

## Cara Menggunakan
1. Jalankan aplikasi Streamlit dengan perintah berikut:

```bash
streamlit run aes2.py
```

2. Akses aplikasi di browser Anda pada URL yang ditampilkan, biasanya `http://localhost:8501`.
3. Upload file Excel yang berisi S-Box.
   - File harus berisi nilai S-Box dalam satu kolom atau satu baris tanpa header.
4. Pilih parameter analisis yang diinginkan di menu samping.
5. Lihat hasil analisis di bagian hasil.
6. Unduh hasil analisis dalam format Excel dengan menekan tombol "Download Results."

## Format Input
File Excel yang diunggah harus memenuhi format berikut:
- Satu kolom atau baris dengan nilai S-Box.

## Hasil
Hasil analisis akan disajikan dalam tabel dan dapat diunduh sebagai file Excel. Parameter yang dihitung meliputi:
- Nonlinearity (NL)
- Strict Avalanche Criterion (SAC)
- Linear Approximation Probability (LAP)
- Differential Approximation Probability (DAP)
- BIC Nonlinearity (BIC-NL)
- BIC Strict Avalanche Criterion (BIC-SAC)

## Catatan
- Perhitungan dapat memakan waktu lebih lama untuk S-Box yang besar.

## Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).
